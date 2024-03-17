# /source/game.py

import arcade

from .enemy import Enemy


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

    def on_show_view(self) -> None:
        self.scene = arcade.Scene()

        self.scene.add_sprite(
            "Enemy",
            Enemy(
                [(100, 100), (200, 100), (300, 300), (500, 100), (700, 200)]
            ),
        )

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

    def on_update(self, delta_time: float) -> None:
        self.scene.on_update(delta_time)
