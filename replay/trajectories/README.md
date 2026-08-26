# Replay Trajectories

고정 동작의 관절 trajectory 기록 파일을 이 폴더에 둔다.
관절값 기록은 용량이 작으므로 git에 포함한다.

## 필요한 trajectory 목록 (시나리오 기준)

| 이름 | 동작 |
|---|---|
| `place_on_table` | 꺼낸 옷을 작업대 위에 내려놓기 |
| `lift_after_grasp` | 양팔 파지 후 들어올리기 |
| `lower_and_flip` | 내려놓은 뒤 뒤집어서 다시 파지 |
| `sort_pass` | 검수 합격 분류 위치로 이동 |
| `sort_fail` | 검수 불합격 분류 위치로 이동 |

## 파일 형식

기록 도구를 정한 뒤 여기에 확정 형식을 적을 것.
(예상: 타임스탬프 + 양팔 관절값 배열의 시계열. JSON 또는 CSV)
