"""RDK X5 통신 클라이언트 — z축·턴테이블 명령/상태. 상세: README.md"""


class RDKClient:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def connect(self) -> None:
        raise NotImplementedError

    def lift_to(self, position: str) -> None:
        """z축을 프리셋 위치("work"/"inspect")로 이동시키고 완료까지 대기한다."""
        raise NotImplementedError

    def rotate_turntable(self, degrees: float) -> None:
        """턴테이블을 지정 각도만큼 회전시키고 완료까지 대기한다."""
        raise NotImplementedError

    def status(self) -> dict:
        """현재 z축 위치·턴테이블 각도·에러 상태를 조회한다."""
        raise NotImplementedError

    def disconnect(self) -> None:
        raise NotImplementedError
