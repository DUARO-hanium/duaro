# web

시연용 **모니터링 전용** 웹 인터페이스 (제어 기능 없음).
WSL에서 서버를 띄우면 윈도우 브라우저에서 `http://localhost:<port>`로 접속된다.

화면에 표시할 것:

- 카메라 실시간 영상 + grasp point 후보/선택 오버레이
- grasp **선택 이유 자막** (`GraspSelection.reason`)
- 현재 파이프라인 단계, 검수 결과, 로그

## 구성

| 파일 | 역할 |
|---|---|
| `state.py` | 파이프라인 ↔ 웹 공유 상태(`Monitor`). 파이프라인이 쓰고 웹은 읽기만 한다 |
| `server.py` | FastAPI 서버. main.py가 백그라운드 스레드로 실행 |

## 구현할 것

- `Monitor`의 `update()`/`log()`/`snapshot()` — 파이프라인 스레드와 웹 스레드가
  동시 접근하므로 스레드 안전하게
- FastAPI 라우트
  - `GET /`: 대시보드 페이지
  - `GET /video`: MJPEG 스트림 — `snapshot().frame`에 grasp 오버레이를 그려서 송출
  - `GET /api/state`: 상태 JSON (phase, selection_reason, inspection_result, messages) — 프론트 폴링용
- `start_in_background()`: uvicorn을 데몬 스레드로 실행
