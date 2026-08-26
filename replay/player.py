"""고정 동작 재생 — 기록된 관절 trajectory 재생. 상세: README.md"""


class ReplayPlayer:
    def __init__(self, trajectory_dir: str) -> None:
        self.trajectory_dir = trajectory_dir

    def connect(self) -> None:
        raise NotImplementedError

    def play(self, name: str) -> None:
        """이름으로 trajectory를 찾아 재생하고 완료까지 대기한다 (blocking)."""
        raise NotImplementedError

    def disconnect(self) -> None:
        raise NotImplementedError
