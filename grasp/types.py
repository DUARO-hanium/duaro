"""grasp 모듈 공용 데이터 타입. 상세: README.md"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GraspCandidate:
    """grasp point 후보 하나 (이미지 픽셀 좌표계)."""

    u: int
    v: int
    score: float       # 모델 신뢰도
    keypoint: str = "" # CPN 키포인트 이름 (예: 소매 끝, 밑단 등 — 모델 출력 기준)


@dataclass
class GraspSelection:
    """양 끝 두 점 선택 결과. reason은 웹 자막으로 노출된다."""

    left: Optional[GraspCandidate]   # 왼팔이 잡을 점
    right: Optional[GraspCandidate]  # 오른팔이 잡을 점
    reason: str

    @property
    def ok(self) -> bool:
        """양 끝 두 점이 모두 선택되었는지 — False면 뒤척임 후 재시도."""
        return self.left is not None and self.right is not None
