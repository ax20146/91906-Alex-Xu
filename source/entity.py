# entity.py

from abc import ABC, abstractmethod
from math import atan2, cos, sin
from typing import ClassVar

from .utils import Sprite, Vector


class PathEntity(Sprite, ABC):
    waypoints: ClassVar[tuple[Vector, ...]]

    def __init__(
        self,
        filename: str,
        speed: int,
        health: int,
    ) -> None:
        super().__init__(
            filename=filename,
            position=self.waypoints[0].convert(),
        )

        self.speed: int = speed
        self.health: int = health

        self.target: int = 0

    def move(self, dt: float) -> None:
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        angle: float = atan2(target.x - position.x, target.y - position.y)

        self.center_x += self.speed * sin(angle) * dt
        self.center_y += self.speed * cos(angle) * dt

    def select_target(self) -> None:
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        if target - 3 < position < target + 3:
            self.target += 1

    def dead(self) -> bool:
        if self.health > 0:
            return False

        self.kill()
        return True

    def on_update(self, dt: float) -> None:
        if self.dead():
            return

        self.face_point(self.waypoints[self.target].convert())
        self.move(dt)
        self.select_target()

        if self.target >= len(self.waypoints):
            self.attack()

    @abstractmethod
    def attack(self) -> None:
        raise NotImplementedError
