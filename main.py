"""DUARO E2E 파이프라인 오케스트레이터 — 시연 시나리오를 상태머신으로 순차 실행한다.

단계 목록과 각 단계의 담당 모듈은 Phase enum과 아래 메서드 참조.
시나리오·모듈 구성 설명은 루트 README.md.

실행 (WSL, ROS2 source + MoveIt 스택 실행 후):
  python main.py
"""

from enum import Enum, auto
from pathlib import Path

import yaml

from act_policy import ACTRunner
from camera import CameraStream
from grasp import detect_candidates, select_grasp_pair
from grasp.detector import load_model as load_grasp_model
from inspection import Inspector
from motion import MoveItClient, uv_to_world
from motion.transform import load_calibration
from rdk_client import RDKClient
from replay import ReplayPlayer
from web import monitor
from web import server as web_server


class Phase(Enum):
    BAG_PICK = auto()        # [ACT]    봉투 벌리기 + 의류 꺼내기
    TRANSFER = auto()        # [RDK]    z축 이동 + 턴테이블 회전
    PLACE_ON_TABLE = auto()  # [Replay] 작업대 위에 옷 내려놓기
    GRASP_DETECT = auto()    # [Grasp]  후보 추출 + 양 끝 선택
    SHUFFLE = auto()         # [미정]   뒤척임 (선택 실패 시)
    GRASP_EXECUTE = auto()   # [MoveIt] uv→world 변환 후 양팔 파지
    LIFT_FRONT = auto()      # [Replay+RDK] 들어올려 검수 높이로
    INSPECT_FRONT = auto()   # [검수]   앞면
    FLIP = auto()            # [Replay] 내려놓고 뒤집어 다시 파지·상승
    INSPECT_BACK = auto()    # [검수]   뒷면
    SORT = auto()            # [Replay] 결과에 따라 분류 (위치만 다름)
    DONE = auto()


def load_settings() -> dict:
    path = Path(__file__).parent / "configs" / "settings.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


class Pipeline:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.camera = CameraStream(cfg["camera"]["frame_dir"])
        self.act = ACTRunner(cfg["act"])
        self.rdk = RDKClient(cfg["rdk"]["host"], cfg["rdk"]["port"])
        self.replay = ReplayPlayer(cfg["replay"]["trajectory_dir"])
        self.moveit = MoveItClient()
        self.inspector = Inspector(cfg["inspection"]["weights"])
        self.grasp_model = None
        self.calib = None
        self.inspection_results: list = []  # front/back 결과 — SORT에서 사용

    def _enter(self, phase: Phase) -> None:
        monitor.update(phase=phase.name)
        monitor.log(f"단계 시작: {phase.name}")

    # ------------------------------------------------------------------
    # 단계
    # ------------------------------------------------------------------

    def bag_pick(self) -> None:
        self._enter(Phase.BAG_PICK)
        self.act.run()

    def transfer(self) -> None:
        self._enter(Phase.TRANSFER)
        # TODO: 시연 동선 확정 후 위치·각도 지정
        self.rdk.lift_to("work")
        self.rdk.rotate_turntable(0.0)

    def place_on_table(self) -> None:
        self._enter(Phase.PLACE_ON_TABLE)
        self.replay.play("place_on_table")

    def grasp_detect(self):
        max_retries = self.cfg["pipeline"]["max_grasp_retries"]
        for attempt in range(1, max_retries + 1):
            self._enter(Phase.GRASP_DETECT)
            frame = self.camera.get_frame()
            candidates = detect_candidates(self.grasp_model, frame)
            selection = select_grasp_pair(candidates)

            monitor.update(
                grasp_candidates=[(c.u, c.v, c.score) for c in candidates],
                selected_grasp=selection if selection.ok else None,
                selection_reason=selection.reason,
            )

            if selection.ok:
                return selection

            monitor.log(f"grasp 선택 실패 ({attempt}/{max_retries}): {selection.reason}")
            self.shuffle()

        raise RuntimeError(f"grasp point 선택 {max_retries}회 실패 — 시나리오 중단")

    def shuffle(self) -> None:
        self._enter(Phase.SHUFFLE)
        raise NotImplementedError("뒤척임 구현 방식 미정 (Replay 또는 ACT)")

    def grasp_execute(self, selection) -> None:
        self._enter(Phase.GRASP_EXECUTE)
        left_xyz = uv_to_world(self.calib, selection.left.u, selection.left.v)
        right_xyz = uv_to_world(self.calib, selection.right.u, selection.right.v)
        self.moveit.move_to("left", left_xyz)
        self.moveit.move_to("right", right_xyz)
        self.moveit.grip("left", close=True)
        self.moveit.grip("right", close=True)

    def lift_front(self) -> None:
        self._enter(Phase.LIFT_FRONT)
        self.replay.play("lift_after_grasp")
        self.rdk.lift_to("inspect")

    def inspect(self, side: str) -> None:
        self._enter(Phase.INSPECT_FRONT if side == "front" else Phase.INSPECT_BACK)
        frame = self.camera.get_frame()
        result = self.inspector.inspect(frame, side)
        self.inspection_results.append(result)
        monitor.update(inspection_result=result)
        monitor.log(f"검수({side}): {'합격' if result.passed else '불합격'}")

    def flip(self) -> None:
        self._enter(Phase.FLIP)
        self.rdk.lift_to("work")
        self.replay.play("lower_and_flip")
        self.rdk.lift_to("inspect")

    def sort(self) -> None:
        self._enter(Phase.SORT)
        all_passed = all(r.passed for r in self.inspection_results)
        self.rdk.lift_to("work")
        self.replay.play("sort_pass" if all_passed else "sort_fail")

    # ------------------------------------------------------------------
    # 전체 실행
    # ------------------------------------------------------------------

    def setup(self) -> None:
        self.grasp_model = load_grasp_model(self.cfg["grasp"]["weights"])
        self.calib = load_calibration(self.cfg["calibration"]["dir"])
        self.inspector.load()
        self.camera.start()
        self.rdk.connect()
        self.replay.connect()
        self.moveit.connect()
        web_server.start_in_background(self.cfg["web"]["host"], self.cfg["web"]["port"])

    def run(self) -> None:
        self.bag_pick()
        self.transfer()
        self.place_on_table()
        selection = self.grasp_detect()
        self.grasp_execute(selection)
        self.lift_front()
        self.inspect("front")
        self.flip()
        self.inspect("back")
        self.sort()
        monitor.update(phase=Phase.DONE.name)
        monitor.log("시나리오 완료")

    def teardown(self) -> None:
        self.camera.stop()
        self.rdk.disconnect()
        self.replay.disconnect()
        self.moveit.disconnect()


def main() -> None:
    cfg = load_settings()
    pipeline = Pipeline(cfg)
    pipeline.setup()
    try:
        pipeline.run()
    finally:
        pipeline.teardown()


if __name__ == "__main__":
    main()
