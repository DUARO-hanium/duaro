# camera

윈도우에서 캡처·저장된 카메라 프레임을 WSL에서 읽어 다른 모듈에 공급하는 **유일한 카메라 창구**.
grasp·inspection·web은 카메라를 직접 열지 않고 전부 `CameraStream.get_frame()`으로 프레임을 받는다.

카메라를 usbipd로 WSL에 직결하면 ~2fps밖에 안 나오는 문제가 있어,
**윈도우 쪽에서 캡처해 파일로 저장하고 WSL이 공유 경로에서 읽는 방식**을 사용한다.

## 구현할 것

- **윈도우 캡처·저장 프로그램** (별도, 윈도우에서 실행) — 저장 경로·파일 형식·갱신 주기를 정하고
  `configs/settings.yaml`의 `camera.frame_dir`에 WSL 기준 경로(`/mnt/c/...`)를 기입
- **`CameraStream`** (`frame_source.py`)
  - `start()`: 공유 디렉토리 감시 시작
  - `get_frame()`: 최신 프레임(BGR) 반환 — 쓰다 만 파일을 읽지 않도록 완성된 최신 파일 판별 필요
  - `stop()`
- 카메라를 여러 대(손목/외부) 쓰게 되면 카메라 구분 인자 추가
