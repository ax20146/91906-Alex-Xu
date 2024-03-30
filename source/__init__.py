from arcade import Window

from .menu import Menu
from .utils.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH

__all__: list[str] = [
    "Window",
    "create_window",
]


def create_window() -> Window:
    window: Window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  # type: ignore
    window.show_view(Menu())

    return window
