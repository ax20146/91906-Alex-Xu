from typing import Literal

import arcade

from .game import Game


class Button(arcade.Sprite):
    def __init__(
        self, position: Literal["Center", "Left", "Right"], view: arcade.View
    ):
        super().__init__("./assets/Slot.png")

        self.view = view
        self.position = (960 // 2, 640 // 2)

        if position == "Left":
            self.center_x -= self.width * 2
        elif position == "Right":
            self.center_x += self.width * 2

    def on_click(self):
        arcade.get_window().show_view(self.view)


class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene: arcade.Scene

    def on_show_view(self):
        arcade.set_background_color((100, 100, 100))
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("UI")
        self.scene.add_sprite("UI", Button("Left", Game("./maps/Plains.tmx")))

    def on_draw(self):
        self.clear()
        self.scene.draw()  # type: ignore

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if sprites := arcade.get_sprites_at_point((x, y), self.scene["UI"]):
            sprite: Button = sprites[-1]  # type: ignore
            self.hover = sprite

        self.hover = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and (
            sprites := arcade.get_sprites_at_point((x, y), self.scene["UI"])
        ):
            sprite: Button = sprites[-1]  # type: ignore
            sprite.on_click()

    def on_update(self, delta_time: float):
        self.scene.on_update(delta_time)
