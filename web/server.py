"""모니터링 웹 서버. 라우트 구성·구현 지침: README.md"""

import threading


def create_app():
    """FastAPI 앱을 생성한다 (라우트: / , /video, /api/state)."""
    raise NotImplementedError


def start_in_background(host: str, port: int) -> threading.Thread:
    """웹 서버를 데몬 스레드로 띄우고 스레드 핸들을 반환한다."""
    raise NotImplementedError
