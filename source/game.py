# /source/game.py

import arcade


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

    def on_show_view(self) -> None:
        self.scene = arcade.Scene()

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

    def on_update(self, delta_time: float) -> None:
        self.scene.on_update(delta_time)
