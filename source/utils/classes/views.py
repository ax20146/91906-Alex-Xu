# /utils/classes/views.py
"""`View` module containing the custom `View` class."""


# Import Built-in Dependencies
from typing import Any

# Import 3rd-Party Dependencies
import arcade


# Define View class
class View(arcade.View):
    """`View` object represents a view (menu/state) of the game.

    Inherited from `arcade.View`.

    Overrides the function definition signature of the `arcade.View`.
    NOTE: `View` does nothing functionality different to `arcade.View`.
    """

    def __init__(self) -> None:
        """Initialise a `View` object."""
        super().__init__()

    def on_draw(self) -> None:
        """OVERRIDE: The draw function called every cycle (tick)."""
        pass

    def on_update(self, delta_time: float) -> None:
        """OVERRIDE: The update function called every cycle (tick).

        Args:
            delta_time (float): The delta time since last tick.
        """
        pass

    def on_mouse_press(self, x: int, y: int, button: int, *args: Any) -> None:
        """OVERRIDE:
        The mouse press event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
            button (int): The mouse button that pressed.
        """
        pass

    def on_mouse_motion(self, x: int, y: int, *args: Any) -> None:
        """OVERRIDE:
        The mouse motion event function called.

        Args:
            x (int): The x position of mouse press.
            y (int): The y position of mouse press.
        """
        pass
