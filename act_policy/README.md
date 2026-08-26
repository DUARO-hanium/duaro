# act_policy

시나리오의 **봉투 벌리기(왼팔) + 의류 꺼내기(오른팔)** 구간을 학습된 ACT 정책으로 수행하는 모듈.

## 구조 (LeRobot 기반)

학습·추론 인프라는 별도 레포 `lerobot-ACT-train-inference-GPUserver`에 있다:

```
윈도우 카메라 → WSL ROS2 → SSH 터널 → GPU 서버 PolicyServer
        follower 상태 ←── action chunk ←──┘
               ↓
      ROS2 OMX follower 컨트롤러
```

추론은 GPU 서버의 PolicyServer가 담당하고, 로봇 구동은 ROS2를 경유한다
(로봇 시리얼 포트는 ROS2 bringup이 소유 — 이 모듈이 직접 잡지 않는다).
추론 서버를 어디에 둘지(원격 GPU 서버 유지 여부)는 미정.

## 구현할 것

- `ACTRunner.run()` — ACT 레포의 추론 클라이언트를 실행·관리하고 태스크 완료까지 대기
  (클라이언트를 서브프로세스로 띄우는 래퍼 형태가 될 가능성이 큼)
- 태스크 완료 판단 기준 (고정 스텝 수 / 정책 출력 / 수동 확인)
- 체크포인트·서버 접속 정보는 `configs/settings.yaml`의 `act` 항목으로 관리
