# /source/__init__.py


from arcade import Window

from .game import MenuView
from .utils import SCREEN_SIZE


def create_window() -> Window:
    window: Window = Window(*SCREEN_SIZE)  # type: ignore
    window.show_view(MenuView())

    return window


__all__: list[str] = ["Window"]
