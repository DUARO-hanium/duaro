# duaro

duaro 시스템 end-to-end 동작 pipeline.

봉투에서 의류를 꺼내 작업대에 펼치고, grasp point를 잡아 들어올려 검수한 뒤 분류하는
전체 시연 시나리오를 하나의 파이프라인으로 실행한다.

## 시연 시나리오

1. **[ACT]** 왼팔로 봉투 벌리기 + 오른팔로 의류 꺼내기
2. **[RDK X5]** z축 이동 + 턴테이블 회전
3. **[Replay]** 작업대 위에 옷 내려놓기
4. **[Grasp]** grasp point 후보 추출 → 옷 양 끝 두 점 선택 (선택 이유는 웹 화면 자막으로 표시)
   - 양 끝 선택 실패 시: 뒤척임 후 재시도
5. **[MoveIt]** (u,v) → world 좌표 변환 후 양팔로 양 끝 파지
6. **[Replay + RDK X5]** 들어올려 검수 높이로
7. **[검수]** 앞면 검수 → 뒤집기 → 뒷면 검수 (결과는 웹 화면에 실시간 표시)
8. **[Replay]** 검수 결과에 따라 분류 (합격/불합격은 내려놓는 위치만 다름)

## 폴더 구조

각 폴더의 역할과 구현할 것은 **해당 폴더의 README.md** 참고.

```
duaro/
├── main.py          # E2E 오케스트레이터 (시나리오 상태머신) — 진입점
├── calibration/     # 사전 셋팅 도구 + 산출물 (카메라 호모그래피 등 — 실행 중엔 안 돌아감)
├── configs/         # settings.yaml
├── camera/          # 카메라 프레임 공급 (윈도우 캡처·저장 → WSL이 공유 경로에서 읽기)
├── act_policy/      # ACT 정책 실행 (LeRobot 기반, GPU 서버 추론)
├── rdk_client/      # RDK X5 통신 (z축·턴테이블)
├── grasp/           # grasp point 후보 추출 + 양 끝 선택
├── motion/          # (u,v)→world 변환 + MoveIt 클라이언트 (ROS2를 쓰는 유일한 모듈)
├── replay/          # 고정 동작 재생 + trajectory 데이터
├── inspection/      # 검수 모델
└── web/             # 모니터링 웹 (모니터링 전용, 제어 없음)
```

설계 원칙:

- **순수 Python 구조** — colcon 워크스페이스가 아니다. ROS2 접점은 `motion/` 내부로 한정.
- **로봇 시리얼 포트는 ROS2 bringup이 상시 소유** — ACT와 MoveIt 모두 그 위에서
  명령을 발행하며, `main.py`가 단계 순서로 배타성을 보장한다.
- **카메라는 `camera/`만 접근** — 나머지 모듈은 `CameraStream.get_frame()`으로 프레임을 받는다.

## 실행 순서

```bash
# 1. (윈도우) 카메라 캡처·저장 프로그램 실행
# 2. (WSL, 별도 터미널) ROS2 source 후 로봇 bringup + MoveIt 스택 실행
# 3. (WSL) 파이프라인 실행
python main.py
# 4. (윈도우 브라우저) http://localhost:8000 에서 모니터링
```

RDK X5에는 z축·턴테이블 명령 서버가 먼저 떠 있어야 한다 (보드 내 코드).

실행 환경: 팀은 용도별로 환경을 나눠 쓴다 — conda `lerobot`(순수 CV·캘리브레이션),
`rosenv`(시스템 Python + ROS2, bringup·MoveIt). `main.py`는 rclpy를 쓰는 `motion/` 때문에
**rosenv 계열(ROS2가 source된 환경)에서 실행**하는 것을 전제로 한다.

## 모델 가중치

grasp 모델, 검수 모델, ACT 체크포인트는 용량 문제로 **git에 포함하지 않는다**
(`weights/` 및 `*.ckpt` 등은 gitignore 처리됨). 팀 공유 드라이브에서 받아
`configs/settings.yaml`에 경로를 지정한다.

## 미확정 항목 (TODO)

- `calibration/`에 캘리브레이션 도구 이관 (`Robot-Action-Pipeline/calibration` → 이 레포)
- 뒤척임(shuffle) 구현 방식: Replay 고정 동작 vs ACT
- ACT 추론 서버 구성 (원격 GPU 서버 유지 여부) — `act_policy/README.md`
- RDK X5 명령 서버 프로토콜·포트, z축 위치 프리셋 (리드·방향 실측 후)
- 윈도우 카메라 캡처 프로그램의 저장 경로·파일 형식
- replay trajectory 기록 도구 및 파일 형식
- 검수 모델 선정
