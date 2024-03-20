from abc import ABC, abstractmethod
from math import atan2, cos, sin
from typing import ClassVar

import arcade

from ..utils import Point, Sprite, Timer, TuplePoint


class PathEntity(Sprite, ABC):
    waypoints: ClassVar[tuple[Point, ...]]

    def __init__(
        self,
        filename: str,
        *,
        speed: int,
        health: int,
    ) -> None:
        super().__init__(
            filename,
            position=self.waypoints[0].convert(),
        )

        self.target: int = 1
        self.speed: int = speed
        self.health: int = health

    def move(self, dt: float) -> None:
        position: Point = Point(*self.position)
        target: Point = self.waypoints[self.target]

        angle: float = -atan2(target.x - position.x, target.y - position.y)

        self.center_x -= self.speed * sin(angle) * dt
        self.center_y += self.speed * cos(angle) * dt

    def toward_target(self):
        self.face_point(self.waypoints[self.target].convert())

    def update_target(self):
        position: Point = Point(*self.position)
        target: Point = self.waypoints[self.target]

        if position.within(target, range=3):
            self.target += 1

    def on_update(self, dt: float) -> None:
        if self.health <= 0:
            self.kill()
            return self.on_die()

        self.move(dt)
        self.toward_target()
        self.update_target()

        if self.target >= len(self.waypoints):
            self.kill()

    @abstractmethod
    def on_die(self) -> None:
        raise NotImplementedError


class TurretEntity(Sprite, ABC):
    targets: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        filename: str,
        position: TuplePoint,
        *,
        damage: int,
        range: int,
        cooldown: int,
    ) -> None:
        super().__init__(
            filename,
            position=position,
        )

        self.damage: int = damage
        self.range: int = range

        self.timer: Timer = Timer(cooldown, self.clock)
        self.reload: Timer = Timer(cooldown // 3, self.clock)

        self.target: PathEntity

    def update_target(self) -> PathEntity | None:
        if (data := arcade.get_closest_sprite(self, self.targets)) is None:
            return

        sprite, distance = data
        if not isinstance(sprite, PathEntity) or distance > self.range:
            return

        return sprite

    def on_update(self, dt: float) -> None:
        if (target := self.update_target()) is None:
            return
        self.target = target

        if not self.reload.available():
            return
        self.face_point(self.target.position)

        if self.timer.available():
            self.timer.update()
            self.reload.update()
            return self.attack()

    @abstractmethod
    def attack(self) -> None:
        raise NotImplementedError
