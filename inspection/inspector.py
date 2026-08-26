"""의류 검수 — 들어올린 옷의 불량 판정. 상세: README.md"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class InspectionResult:
    """한 면에 대한 검수 결과."""

    passed: bool
    side: str                # "front" 또는 "back"
    defects: list = field(default_factory=list)  # 불량 목록 (형식은 모델 확정 후 정의)
    score: float = 0.0


class Inspector:
    def __init__(self, weights_path: str) -> None:
        self.weights_path = weights_path

    def load(self) -> None:
        """검수 모델을 메모리에 로드한다."""
        raise NotImplementedError

    def inspect(self, frame: np.ndarray, side: str) -> InspectionResult:
        """프레임 한 장에 대해 검수를 수행한다."""
        raise NotImplementedError
