# /__init__.py
"""Package for the game."""


# Import 3rd-Party Dependencies
from arcade import Window

# Import Local Dependencies
from .utils.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from .views.menu import Menu

# Export classes & function to run game
__all__: list[str] = [
    "Window",
    "create_window",
]


# Define window factory function
def create_window() -> Window:
    """Create an instance of the game.

    Returns:
        Window: The game window.
    """

    window: Window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(Menu())

    return window
