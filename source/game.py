# /source/game.py

import arcade

from .enemy import Enemy
from .tower import Tower
from .vector import Vector


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

        self.health: int
        self.waypoint: tuple[Vector, ...]

    def on_show_view(self) -> None:
        self.scene = arcade.Scene()

        Enemy.waypoints = tuple(
            Vector(*point)
            for point in [
                (100, 100),
                (200, 100),
                (300, 300),
                (500, 100),
                (700, 200),
            ]
        )

        tower = Tower()
        tower.position = 300, 400

        self.scene.add_sprite("Tower", tower)
        self.scene.add_sprite("Enemy", Enemy())
        e = Enemy()
        e.speed = 200

        self.scene.add_sprite("Enemy", e)

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

    def on_update(self, delta_time: float) -> None:
        Tower.targets = self.scene.get_sprite_list("Enemy")

        self.scene.on_update(delta_time)
