# Import Dependencies
from abc import ABC, abstractmethod
from math import atan2, cos, sin
from typing import ClassVar

from ..utils import Sprite, Vector


class PathEntity(Sprite, ABC):
    waypoints: ClassVar[tuple[Vector, ...]]

    def __init__(
        self,
        filename: str,
        speed: int,
        health: int,
    ) -> None:
        super().__init__(
            filename,
            position=self.waypoints[0].convert(),
        )

        self.speed: int = speed
        self.health: int = health

        self.target: int = 1

    def is_dead(self) -> bool:
        return self.health <= 0

    def move(self, dt: float):
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        angle: float = -atan2(target.x - position.x, target.y - position.y)

        self.center_x -= self.speed * sin(angle) * dt
        self.center_y += self.speed * cos(angle) * dt

    def toward_target(self) -> None:
        self.face_point(self.waypoints[self.target].convert())

    def update_target(self) -> None:
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        if position.within(target, range=3):
            self.target += 1

    def on_update(self, dt: float) -> None:
        if self.is_dead():
            self.on_die()
            return

        self.move(dt)
        self.toward_target()
        self.update_target()

        if self.target >= len(self.waypoints):
            self.on_end()

    @abstractmethod
    def on_die(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_end(self) -> None:
        raise NotImplementedError
