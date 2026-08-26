# motion

선택된 grasp point의 **픽셀 좌표를 로봇 world 좌표로 변환**하고,
**MoveIt으로 trajectory를 계산·실행해 양팔로 파지**하는 모듈.
이 레포에서 ROS2(rclpy)를 사용하는 유일한 모듈이다.

## 좌표 변환 (`transform.py`)

캘리브레이션은 이 레포의 `calibration/camera`에서 수행하며,
산출물은 **평면 가정 호모그래피** 방식이다 (RGB 단안, depth 없음):

- `H_table.json`: 작업대 평면 픽셀 → world 변환 행렬 H(3×3) + 평면 높이 `plane_z`
- `intrinsics.json`: 카메라 내부 파라미터 K·왜곡계수 dist (왜곡 보정을 쓴 경우만)

변환은 `(u, v) → H → (x, y)`, `z = plane_z` (TABLE_Z 실측값).
⚠️ 왜곡 보정된 H(`"undistorted": true`)를 쓰면 픽셀도 `cv2.undistort`한 이미지에서 뽑아야 한다.

## MoveIt 클라이언트 (`moveit_client.py`)

MoveIt 본체(move_group)·로봇 bringup·RViz는 이 레포 코드가 아니라 **별도 launch로 미리 띄워두는
프로그램**이며, 로봇 시리얼 포트는 bringup이 상시 소유한다. 이 모듈은 이미 떠 있는
move_group에 rclpy로 목표를 보내는 클라이언트일 뿐이다.

## 구현할 것

- `load_calibration()`: H·plane_z (+K·dist) 로드
- `uv_to_world()`: 호모그래피 적용 → `[x, y, plane_z]`
- `MoveItClient`: `connect()`(rclpy 초기화·move_group 연결), `move_to(arm, xyz)`,
  `grip(arm, close)` — 파지 자세(orientation)는 고정값으로 시작
- 첫 실행 시 z 마진 규칙 준수 (목표보다 2~3cm 위에서 단계적으로 하강 — 캘리브레이션 레포 README 참고)
