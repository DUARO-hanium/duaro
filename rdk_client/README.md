# rdk_client

z축 리프트(STS-3215)와 턴테이블을 제어하기 위해 **RDK X5 보드와 통신**하는 클라이언트.

실제 모터 제어 코드는 RDK X5 안의 `zaxis_lift` 패키지가 담당한다.
이 모듈은 명령("z축 검수 높이로", "턴테이블 90도")을 보내고 완료/상태 응답을 받을 뿐,
모터를 직접 구동하지 않는다.

## 구현할 것

- **RDK X5 쪽 명령 서버** (보드 내, 별도 작업) — TCP 프로토콜·포트를 정해서
  `configs/settings.yaml`의 `rdk` 항목에 기입
- **`RDKClient`** (`client.py`)
  - `connect()` / `disconnect()`
  - `lift_to(position)`: 위치 이름(`"work"`, `"inspect"`)으로 z축 이동, 완료까지 blocking.
    실제 높이 값은 보드 쪽에 프리셋으로 정의 (리드·방향 실측 후 확정)
  - `rotate_turntable(degrees)`: 완료까지 blocking
  - `status()`: 현재 위치·각도·에러 조회
