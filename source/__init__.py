# /source/__init__.py


from arcade import Window

from .menu import Menu
from .utils.constants import Screen


def create_window() -> Window:
    window: Window = Window(*Screen.SIZE)  # type: ignore
    window.show_view(Menu())

    return window


__all__: list[str] = ["Window"]
