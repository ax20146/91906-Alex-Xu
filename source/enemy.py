# /source/enemy.py


import math

import arcade

from .utils import ArcadePoint, Point


class Enemy(arcade.Sprite):
    def __init__(self, waypoints: list[ArcadePoint]) -> None:
        super().__init__(":resources:images/topdown_tanks/tankBody_dark.png")

        self.speed = 100

        self.waypoints: list[Point] = [
            Point(*waypoint) for waypoint in waypoints
        ]
        self.target: int = 1

        self.position = self.waypoints[0].convert()

    @property
    def can_move(self) -> bool:
        return self.target < len(self.waypoints)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if not self.can_move:
            return

        self.move(delta_time)
        self.face_point(self.waypoints[self.target].convert())

        if (
            Point(*self.position).round(-1)
            == self.waypoints[self.target].round()
        ):
            self.target += 1

    def move(self, dt: float):
        position: Point = Point(*self.position)
        target: Point = self.waypoints[self.target]

        angle: float = math.atan2(
            target.x - position.x, target.y - position.y
        )

        self.center_x += self.speed * math.sin(angle) * dt
        self.center_y += self.speed * math.cos(angle) * dt
