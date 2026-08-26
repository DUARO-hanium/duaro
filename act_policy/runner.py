"""ACT 정책 실행 — 봉투 벌리기 + 의류 꺼내기. 구조 설명: README.md"""


class ACTRunner:
    def __init__(self, config: dict) -> None:
        """config: settings.yaml의 act 항목 (체크포인트·추론 서버 접속 정보 등)."""
        self.config = config

    def run(self) -> None:
        """봉투 벌리기 → 의류 꺼내기 태스크를 완료할 때까지 실행한다 (blocking)."""
        raise NotImplementedError
