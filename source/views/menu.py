# /views/menu.py
"""`Menu` module containing the `Menu` class."""


# Import 3rd-Party Dependencies
import arcade
import arcade.gui

# Import Local Dependencies
from ..utils import Clock, Timer, View
from ..utils.constants import (
    ANCHOR_BOTTOM,
    ANCHOR_CENTER,
    ANCHOR_TOP,
    BLACK,
    DEFAULT_DATA,
    FONT,
    FONT_LARGE,
    FONT_MEDIUM,
    FONT_TITLE,
    GREY,
    SCREEN_HALF_H,
    SCREEN_HALF_W,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TIPS_COOLDOWN,
    TIPS_DATA,
    TRANSPARENT_DARK,
    WHITE,
)
from ..utils.functions import generate_tips, read_data, write_data
from ..utils.types import Any, Callable, Iterator
from . import game


# Define Menu class
class Menu(View):
    """`Menu` view represents the game menu view.

    Inherited from `View`.

    Implements the functionality of the game menu view.
    """

    def __init__(self) -> None:
        """Initialise a `Menu` view object."""

        # Initialised parent class
        super().__init__()

        # Define view's scene & ui
        self.ui: arcade.gui.UIManager = arcade.gui.UIManager()
        self.scene: arcade.Scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap("./maps/Hard.tmx")
        )

        # Define display, clock, timer info of the view
        self.display: str = TIPS_DATA[0]
        self.clock: Clock = Clock()
        self.timer: Timer = Timer(self.clock, TIPS_COOLDOWN)

        # Instantiate buttons based on the game progression data
        buttons: Iterator[arcade.gui.UIPadding] = (
            Button(
                tilemap.title(),
                lambda tilemap: self.window.show_view(game.Game(tilemap)),
                disabled=not unlocked,
                args=tilemap.title(),
            ).with_space_around(top=FONT_MEDIUM, bottom=FONT_MEDIUM)
            for tilemap, unlocked in self.load_data().items()
        )

        # Add the buttons to UI manager
        self.ui.add(
            arcade.gui.UIAnchorWidget(
                child=arcade.gui.UIBoxLayout(children=buttons)
            )
        )

    def load_data(self) -> dict[str, bool]:
        """Load the game progression data from disk.

        Returns:
            dict[str, bool]: The game progression data.
        """

        # Read the data file from disk
        try:
            return read_data()
        except FileNotFoundError:
            pass

        # Write a default data if data file doesn't exist
        write_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    def on_show_view(self) -> None:
        """Function called when view is shown."""
        self.ui.enable()

    def on_hide_view(self) -> None:
        """Function called when view is hidden."""
        self.ui.disable()

    def on_draw(self) -> None:
        """The draw function called every cycle (tick)."""

        # Draw scene
        self.clear()
        self.scene.draw()

        # Draw overlay shadow
        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HALF_H,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            color=TRANSPARENT_DARK,
        )

        # Draw the UI
        self.ui.draw()

        # Draw the game title
        arcade.draw_text(
            SCREEN_TITLE,
            SCREEN_HALF_W,
            SCREEN_HEIGHT - FONT_TITLE,
            font_name=FONT,
            font_size=FONT_TITLE,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_TOP,
            color=WHITE,
        )

        # Draw the tips information
        arcade.draw_text(
            self.display,
            SCREEN_HALF_W,
            FONT_LARGE,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_BOTTOM,
            color=WHITE,
        )

    def on_update(self, delta_time: float) -> None:
        """The update function called every cycle (tick).

        Args:
            delta_time (float): The change in time since last tick.
        """

        # Update the clock
        self.clock.update(delta_time)

        # Generate new tip every TIP_COOLDOWN cycle
        if self.timer.available():
            self.display = generate_tips()
            self.timer.update()


class Button(arcade.gui.UIFlatButton):
    """`Button` object represents a UI button.

    Inherited from `arcade.Sprite`.

    Implements & overrides some functionality of
    the `arcade.gui.UIFlatButton`.
    """

    def __init__(
        self,
        text: str,
        on_click: Callable[[str], None],
        *,
        args: str,
        disabled: bool = False,
        width: int = 250,
        height: int = 50,
    ) -> None:
        """Initialise a `Button` object.

        Args:
            text (str): The text displayed on button.
            on_click (Callable[[str], None]):
            The function called when button is clicked.
            args (str): The arguments to the `on_click` function.
            disabled (bool, optional): Whether the button is disabled.
                Defaults to False.
            width (int, optional): The width of the button.
                Defaults to 250.
            height (int, optional): The width of the button.
                Defaults to 50.
        """

        # Define the styles of the button
        style: dict[str, Any] = {
            "font_name": FONT,
            "font_size": FONT_LARGE,
            "border_color_pressed": None,
            "font_color": GREY if disabled else WHITE,
            "font_color_pressed": GREY if disabled else WHITE,
            "bg_color_pressed": BLACK if disabled else TRANSPARENT_DARK,
        }

        # Initialised parent class
        super().__init__(
            text=text,
            width=width,
            height=height,
            style=style,
        )

        # Define public attributes of clock
        self.disabled: bool = disabled
        self.click: Callable[[str], None] = on_click
        self.args: str = args

    def on_click(self, *args: Any) -> None:
        """The function called when button is clicked."""

        if self.disabled:
            return

        # Call the `click` function with arguments if button is active
        self.click(self.args)
