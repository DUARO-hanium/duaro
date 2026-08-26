"""카메라 프레임 공급 — 윈도우가 저장한 프레임을 공유 경로에서 읽는다. 상세: README.md"""

from typing import Optional

import numpy as np


class CameraStream:
    def __init__(self, frame_dir: str) -> None:
        """frame_dir: 윈도우 캡처 프로그램이 프레임을 저장하는 공유 디렉토리 (WSL 기준 경로)."""
        self.frame_dir = frame_dir
        self._latest_frame: Optional[np.ndarray] = None

    def start(self) -> None:
        """공유 디렉토리 감시를 시작하고 최신 프레임을 갱신해둔다."""
        raise NotImplementedError

    def get_frame(self) -> np.ndarray:
        """가장 최근 프레임(BGR)을 반환한다."""
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
