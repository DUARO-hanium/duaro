"""파이프라인 ↔ 웹 공유 상태. 역할·구현 지침: README.md"""

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np


@dataclass
class MonitorState:
    """웹 화면에 표시할 현재 상태 스냅샷."""

    phase: str = "IDLE"                          # 현재 단계 (main.Phase의 name)
    frame: Optional[np.ndarray] = None           # 최신 카메라 프레임 (BGR)
    grasp_candidates: list = field(default_factory=list)  # [(u, v, score), ...] 오버레이용
    selected_grasp: Optional[Any] = None         # 선택된 GraspSelection
    selection_reason: str = ""                   # 선택 이유 (자막용)
    inspection_result: Optional[Any] = None      # InspectionResult
    messages: list = field(default_factory=list)  # 로그 (최근 순)


class Monitor:
    """스레드 안전한 MonitorState 접근자. 파이프라인이 쓰고 웹은 읽는다."""

    def update(self, **kwargs) -> None:
        """상태 필드를 갱신한다. 예: monitor.update(phase="GRASP_DETECT")"""
        raise NotImplementedError

    def log(self, message: str) -> None:
        """로그 메시지를 추가한다."""
        raise NotImplementedError

    def snapshot(self) -> MonitorState:
        """현재 상태의 복사본을 반환한다 (웹에서 읽기 전용)."""
        raise NotImplementedError


# 전역 모니터 인스턴스 — 파이프라인과 웹 서버가 함께 사용
monitor = Monitor()
