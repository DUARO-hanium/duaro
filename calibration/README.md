# calibration

카메라 캘리브레이션 등 **사전 셋팅 도구와 그 산출물**을 두는 곳.
시연 실행 중에 돌아가는 코드가 아니라, 실행 전에 사람이 돌리는 작업이다.
산출물은 여기서 바로 읽히므로(`settings.yaml`의 `calibration.dir`) 별도 복사가 필요 없다.

## 구성 (예정)

```
calibration/
├── camera/   # 픽셀 (u,v) ↔ world 변환용 호모그래피 캘리브레이션
└── motor/    # 모터 캘리브레이션
```

## 할 일

- `Robot-Action-Pipeline/calibration`의 `camera/`, `motor/` 내용(스크립트·절차 README)을 이 폴더로 이관
- 실제 환경에서 캘리브레이션 실행하여 산출물 생성

## camera/ 산출물 (motion/transform.py가 읽음)

| 파일 | 내용 | 생성 스크립트 |
|---|---|---|
| `camera/H_table.json` | 작업대 평면 픽셀→world 호모그래피 H(3×3) + `plane_z` | `aruco_homography.py` |
| `camera/intrinsics.json` | 내부 파라미터 K·왜곡계수 dist (왜곡 보정 쓸 때만) | `checkerboard_intrinsics.py` |

산출물은 실측 데이터이므로 git에 포함한다.
⚠️ 카메라를 옮기거나 재장착하면 H는 무효 — 재캘리브레이션 필수.
