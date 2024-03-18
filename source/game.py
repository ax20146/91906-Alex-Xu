# /source/game.py

import arcade

from .clock import Clock
from .enemy import Enemy
from .tower import Tower
from .utils.vector import Vector


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

        self.health: int
        self.clock = Clock()

    def on_show_view(self) -> None:
        self.scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap("./maps/map1.tmx")
        )

        Enemy.waypoints = tuple(
            Vector(*waypoint.position)
            for waypoint in sorted(
                self.scene.get_sprite_list("Waypoints"),
                key=lambda sprite: sprite.properties["order"],
            )
        )

        self.scene.add_sprite("Enemy", Enemy())
        e = Enemy()
        e.speed = 200
        e.health = 1000

        self.scene.add_sprite("Enemy", e)

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if info := arcade.get_sprites_at_point((x, y), self.scene["Slots"]):
            slot: arcade.Sprite = info[-1]
            self.scene.add_sprite(
                "Tower", Tower((slot.center_x, slot.center_y))
            )

    def on_update(self, delta_time: float) -> None:
        self.clock.update(delta_time)

        Tower.targets = self.scene.get_sprite_list("Enemy")

        self.scene.on_update(delta_time)
