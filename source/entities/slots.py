# /entities/slots.py
"""`Slots` module containing the `Slot` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ..utils import Sprite, Vector
from ..utils.constants import (
    ANCHOR_CENTER,
    BLACK,
    FONT,
    FONT_SMALL,
    MINIMUM_COIN,
    STAT_UI_LARGE_HEIGHT,
    STAT_UI_OFFSET,
    STAT_UI_OUTLINE,
    STAT_UI_WIDTH,
    TRANSPARENT_DARK,
    TRANSPARENT_LIGHT,
    WHITE,
)
from .turrets import towers


# Define Slot class
class Slot(Sprite):
    """`Slot` object represents a slot sprite.

    Inherited from `Sprite`.

    Implements the functionality of a slot sprite.
    """

    # Define class constants
    FILENAME = "./assets/Entities/Slot.png"
    SELL_RATE = 0.75

    def __init__(self, position: Vector) -> None:
        """Initialise a `Slot` sprite object.

        Args:
            position (Vector): The position of sprite.
        """

        # Initialised parent class
        super().__init__(self.FILENAME, position)

        # Define attributes of slot
        self.tower: towers.Tower | None = None

    def on_sell(self) -> int:
        """Event called to sell the tower object.

        Returns:
            int: The coin amount gained from selling.
        """

        if not self.tower:
            return MINIMUM_COIN

        # Selling the tower & return the money
        price = int(self.tower.PRICE * self.SELL_RATE)
        self.tower.kill()
        self.tower = None

        return price

    def on_hover_draw(self) -> None:
        """Event called when slot is hovered."""

        # Draw the tower/slot name
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET,
            width=STAT_UI_WIDTH,
            height=STAT_UI_LARGE_HEIGHT,
            color=TRANSPARENT_DARK,
        )
        arcade.draw_text(
            self.tower.name() if self.tower else self.name(),
            self.x,
            self.y + STAT_UI_OFFSET,
            font_name=FONT,
            font_size=FONT_SMALL,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

        # Outline the slot
        self.draw_hit_box(BLACK, STAT_UI_OUTLINE)

    def on_select_draw(self) -> None:
        """Event called when slot is selected."""

        # Draw the range of tower
        if self.tower:
            arcade.draw_circle_filled(
                self.x,
                self.y,
                radius=self.tower.RANGE,
                color=TRANSPARENT_LIGHT,
            )

        # Draw the tower/slot name
        self.on_hover_draw()
