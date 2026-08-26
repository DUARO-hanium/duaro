"""MoveIt 클라이언트 — 떠 있는 move_group에 rclpy로 목표 전송. 전제 조건: README.md"""

import numpy as np


class MoveItClient:
    def __init__(self) -> None:
        # rclpy 초기화는 connect()에서 — import 시점에 ROS2 의존이 생기지 않게 함
        self._node = None

    def connect(self) -> None:
        """rclpy를 초기화하고 move_group 액션 서버에 연결한다."""
        raise NotImplementedError

    def move_to(self, arm: str, position: np.ndarray) -> None:
        """arm("left"/"right")의 엔드이펙터를 world 좌표 [x,y,z]로 이동시킨다 (blocking)."""
        raise NotImplementedError

    def grip(self, arm: str, close: bool) -> None:
        """그리퍼를 여닫는다."""
        raise NotImplementedError

    def disconnect(self) -> None:
        raise NotImplementedError
