import json
from typing import Any, Callable

import arcade
import arcade.gui

from .game import Game
from .utils.constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    UI_BACKGROUND_COLOUR,
)

ANCHOR_CENTER = "center"
FONT_LARGE = 50
FONT_MEDIUM = 24
FONT = "Kenney Future Narrow"
WHITE = (255, 255, 255)
DARK_GREY = (80, 80, 80)
BLACK = (21, 19, 21)


class Defeat(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, color=UI_BACKGROUND_COLOUR
        )

        arcade.draw_text(
            "Defeat",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            font_size=FONT_LARGE,
            font_name=FONT,
            anchor_x="center",
            anchor_y="center",
        )

    def on_mouse_press(self, *args: Any) -> None:
        self.window.show_view(Menu())


class Victory(arcade.View):
    def __init__(self, map_name: str) -> None:
        super().__init__()

        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, color=UI_BACKGROUND_COLOUR
        )

        arcade.draw_text(
            "Victory",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            font_size=FONT_LARGE,
            font_name=FONT,
            anchor_x="center",
            anchor_y="center",
        )

        data: dict[str, bool] = {}
        with open("./data.json") as json_file:
            data = json.load(json_file)

        lst = list(data)
        idx = lst.index(map_name) + 1
        if idx < len(lst):
            data[lst[idx]] = True

        with open("./data.json", "w") as json_file:
            json.dump(data, json_file)

    def on_mouse_press(self, *args: Any) -> None:
        self.window.show_view(Menu())


class Button(arcade.gui.UIFlatButton):
    def __init__(
        self,
        text: str,
        click: Callable[..., None],
        *,
        disabled: bool = False,
        width: int = 250,
        height: int = 50,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            text=text,
            width=width,
            height=height,
            style={
                "font_name": FONT,
                "font_size": FONT_MEDIUM,
                "border_color_pressed": None,
                "font_color": DARK_GREY if disabled else WHITE,
                "font_color_pressed": DARK_GREY if disabled else WHITE,
                "bg_color_pressed": BLACK if disabled else (*BLACK, 180),
            },
        )

        self.disabled: bool = disabled
        self.click: Callable[..., None] = click
        self.args: dict[str, Any] = kwargs

    def on_click(self, *args: Any) -> None:
        if self.disabled:
            return

        self.click(**self.args)


class Menu(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap("./maps/Hard.tmx"),
        )
        self.ui: arcade.gui.UIManager = arcade.gui.UIManager()
        self.ui.enable()

        ui = arcade.gui.UILabel(
            text=SCREEN_TITLE,
            font_name=FONT,
            font_size=FONT_LARGE,
        )
        self.ui.add(  # type: ignore
            arcade.gui.UIAnchorWidget(child=ui, anchor_y="top", align_y=-50)
        )

        data: dict[str, bool] = {
            "Easy": True,
            "Medium": False,
            "Hard": False,
        }

        try:
            with open("./data.json") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            with open("./data.json", "w") as json_file:
                json.dump(data, json_file)

        ui = arcade.gui.UIBoxLayout(
            children=(
                Button(
                    map_name.title(),
                    lambda map: self.window.show_view(Game(map)),
                    disabled=not unlocked,
                    map=map_name,
                ).with_space_around(top=12, bottom=12)
                for map_name, unlocked in data.items()
            )
        )
        self.ui.add(arcade.gui.UIAnchorWidget(child=ui))  # type: ignore

        info = [
            "Select empty slot to place towers",
            "Right click on a tower to sell",
            "Reinforcements have cooldowns",
            "Click on enemies or reinforcements to permanently view stats",
            "Rocket Launcher is slow, so it could miss the target!",
            "Rocket Launcher deal splash damage",
            "Tower slots are limited so use them wisely!",
            "Coins are attracted to teh cursor within a certain range!",
        ]
        self.info: str = info[0]

        def update_info():
            self.info = random.choice(info)

        import random

        ui = Button(
            "?",
            lambda: update_info(),
            width=FONT_MEDIUM,
            height=FONT_MEDIUM,
        )
        self.ui.add(  # type: ignore
            arcade.gui.UIAnchorWidget(
                child=ui,
                anchor_x="left",
                anchor_y="bottom",
                align_x=FONT_MEDIUM,
                align_y=FONT_MEDIUM,
            )
        )

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()  # type: ignore
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 100)
        )
        self.ui.draw()

        arcade.draw_text(
            self.info,
            SCREEN_WIDTH // 2,
            FONT_MEDIUM,
            font_size=FONT_MEDIUM // 2,
            font_name=FONT,
            anchor_x="center",
            anchor_y="bottom",
        )
