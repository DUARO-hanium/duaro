"""grasp point 선택 — 후보 중 옷 양 끝 두 점을 고른다. 선택 기준: README.md"""

from .types import GraspCandidate, GraspSelection


def select_grasp_pair(candidates: list[GraspCandidate]) -> GraspSelection:
    """양팔이 잡을 두 점을 선택한다. 실패 시 left/right=None, reason에 사유 기재."""
    raise NotImplementedError
