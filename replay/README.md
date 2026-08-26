# replay

미리 기록해둔 관절 trajectory를 그대로 **재생**하는 모듈.
매번 동일한 고정 동작 — 작업대에 옷 내려놓기, 파지 후 들어올리기, 내려놓고 뒤집기,
분류 위치로 옮기기 — 을 담당한다.

trajectory 데이터는 `trajectories/`에 저장한다 (필요한 동작 목록·파일 형식은 그 폴더의 README).

## 구현할 것

- **기록 도구**: 고정 동작을 실제 로봇에서 기록하는 방법 결정 (teleop 등) 및 기록 스크립트
- **`ReplayPlayer`** (`player.py`)
  - `connect()` / `disconnect()`: 로봇 연결 관리
  - `play(name)`: trajectory 이름으로 로드해 재생, 완료까지 blocking
- 재생 경로 결정: ROS2 bringup 위에서 JointTrajectory 발행 vs 직접 제어 — 기록 도구와 맞춰 확정
