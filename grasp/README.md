# grasp

작업대 위 옷 이미지에서 **grasp point 후보를 추출하고, 옷 양 끝 두 점(왼팔·오른팔용)을 선택**하는 모듈.

검출은 `Detection` 레포의 `deep_fashion/fashionai-key-points-detection`(CPN, ailia) 기반 —
의류 카테고리별로 명명된 키포인트와 신뢰도를 출력한다.

선택 결과의 `reason`(왜 이 두 점인지 / 왜 실패했는지)은 시연 때 웹 화면 **자막으로 그대로 노출**되므로
사람이 읽을 수 있는 문장으로 만든다. 양 끝 선택 실패 시 파이프라인은 뒤척임 후 재시도한다.

## 구성

| 파일 | 역할 |
|---|---|
| `types.py` | `GraspCandidate`(u, v, score, 키포인트 이름), `GraspSelection`(left/right/reason) |
| `detector.py` | 모델 로드 + 프레임에서 후보 추출 |
| `selector.py` | 후보들 중 양 끝 두 점 선택 |

## 구현할 것

- `load_model()` / `detect_candidates()`: CPN 키포인트 검출을 후보 리스트로 변환
  (가중치는 git 미포함 — 루트 README 참고)
- `select_grasp_pair()`: 양 끝 판단 기준 확정 — 점 사이 거리, 좌우 배치, 키포인트 종류,
  양팔 작업 공간(reachability). 실패 시에도 reason을 채워서 반환
