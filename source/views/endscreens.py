# /views/endscreens.py
"""`Endscreens` module containing the `Endscreen` class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ..utils import View
from ..utils.constants import (
    ANCHOR_CENTER,
    FONT,
    FONT_TITLE,
    SCREEN_HALF_H,
    SCREEN_HALF_W,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TRANSPARENT_DARK,
    WHITE,
)
from ..utils.functions import process_data, read_data, write_data
from ..utils.types import Any
from . import menu


# Define Endscreen class
class Endscreen(View):
    """`Endscreen` object represents a endscreen view.

    Inherited from `View`.

    Implements the base functionality of a endscreen view.
    """

    def __init__(self, text: str | None = None) -> None:
        """Initialise a `Endscreen` view object.

        Args:
            text (str | None, optional): The endscreen text displayed.
                Defaults to None.
        """

        # Initialised parent class
        super().__init__()

        # Draw transparent background overlay
        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HALF_H,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            color=TRANSPARENT_DARK,
        )

        # Draw endscreen display text
        arcade.draw_text(
            text if text else self.__class__.__name__,
            SCREEN_HALF_W,
            SCREEN_HALF_H,
            font_name=FONT,
            font_size=FONT_TITLE,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def on_mouse_press(self, x: int, y: int, button: int, *args: Any) -> None:
        """The mouse press event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
            button (int): The mouse button that pressed.
        """

        # Return the menu on left click
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.window.show_view(menu.Menu())


# Define Victory class
class Victory(Endscreen):
    """`Victory` object represents a victory endscreen view.

    Inherited from `Endscreen`.

    Implements the functionality of a victory endscreen view.
    """

    def __init__(self, tilemap: str) -> None:
        """Initialise a `Victory` endscreen view object.

        Args:
            tilemap (str): The tilemap name for writing to data file.
        """

        # Initialised parent class
        super().__init__()

        # Writing the game progress data to disk
        write_data(process_data(tilemap, read_data()))


# Define Defeat class
class Defeat(Endscreen):
    """`Defeat` object represents a defeat endscreen view.

    Inherited from `Endscreen`.

    Implements the functionality of a defeat endscreen view.
    """
