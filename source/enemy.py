# /source/enemy.py


import arcade

from .utils.constants import HEALTH_HIGH, SPEED_MEDIUM, VARIABILITY
from .utils.functions import atan2, cos, sin
from .utils.types import ClassVar
from .utils.vector import Vector


class Enemy(arcade.Sprite):
    waypoints: ClassVar[tuple[Vector, ...]]

    def __init__(self, assets: str | None = None) -> None:
        super().__init__(
            ":resources:images/topdown_tanks/tankBody_dark.png"
            if assets is None
            else assets
        )

        self.speed = SPEED_MEDIUM
        self.health: int = HEALTH_HIGH

        self.target: int = 1
        self.position = self.waypoints[0].convert()

    def move(self, dt: float) -> None:
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        angle: float = atan2(target.x - position.x, target.y - position.y)

        self.center_x += self.speed * sin(angle) * dt
        self.center_y += self.speed * cos(angle) * dt

    def update_target(self):
        position: Vector = Vector(*self.position)
        target: Vector = self.waypoints[self.target]

        if target - VARIABILITY < position < target + VARIABILITY:
            self.target += 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        # Check alive
        if self.health <= 0:
            self.kill()
            return

        # Move
        self.face_point(self.waypoints[self.target].convert())
        self.move(delta_time)
        self.update_target()

        # Check reached end
        if self.target >= len(self.waypoints):
            self.kill()
            return
