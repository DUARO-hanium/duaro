"""픽셀 (u,v) → world 좌표 변환 (평면 호모그래피). 산출물 형식: README.md"""

import numpy as np


def load_calibration(calib_dir: str) -> dict:
    """calibration/camera/의 H_table.json(H, plane_z) 등을 로드한다."""
    raise NotImplementedError


def uv_to_world(calib: dict, u: int, v: int) -> np.ndarray:
    """호모그래피로 (u,v) → (x,y), z=plane_z. 반환: [x, y, z] (로봇 베이스 기준, m)."""
    raise NotImplementedError
