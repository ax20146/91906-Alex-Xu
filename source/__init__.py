# /source/__init__.py


from arcade import Window

from .game import Game
from .utils.constants import SCREEN_SIZE


def create_window() -> Window:
    window: Window = Window(*SCREEN_SIZE)  # type: ignore
    window.show_view(Game())

    return window


__all__: list[str] = ["Window"]
