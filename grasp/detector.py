"""grasp point 후보 추출 (CPN 키포인트 검출 기반). 상세: README.md"""

import numpy as np

from .types import GraspCandidate


def load_model(weights_path: str):
    """grasp 추출 모델을 로드한다."""
    raise NotImplementedError


def detect_candidates(model, frame: np.ndarray) -> list[GraspCandidate]:
    """프레임에서 후보 목록을 추출한다. 점수 내림차순, 없으면 빈 리스트."""
    raise NotImplementedError
