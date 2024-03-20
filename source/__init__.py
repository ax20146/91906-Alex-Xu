# /source/__init__.py


from arcade import Window

from .game import Game
from .utils.constants import Screen


def create_window() -> Window:
    window: Window = Window(*Screen.SIZE)  # type: ignore
    window.show_view(Game())

    return window


__all__: list[str] = ["Window"]
