# inspection

z축으로 들어올려 펼쳐진 옷을 카메라 프레임으로 **검수(불량 판정)**하는 모듈.
앞면 검수 → 뒤집기 → 뒷면 검수, 시나리오에서 두 번 호출된다.
결과는 `web.monitor`를 통해 모니터링 화면에 실시간 표시되고,
앞·뒷면 결과를 종합해 분류 위치(합격/불합격)가 정해진다.

## 구현할 것

- **검수 모델 선정·로드** (`Inspector.load()`) — 가중치는 git 미포함 (루트 README 참고)
- **`Inspector.inspect(frame, side)`** → `InspectionResult(passed, side, defects, score)`
- `defects`의 형식(불량 위치·종류) 확정 — 모델 출력에 맞춰 정의, 웹 오버레이 표시에 사용
