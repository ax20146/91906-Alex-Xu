# /entities/buttons.py
"""`Buttons` module containing the `Button` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ..utils import Sprite, Timer, Vector
from ..utils.constants import (
    ANCHOR_CENTER,
    FONT,
    FONT_MEDIUM,
    MINIMUM_COIN,
    TRANSPARENT_LIGHT,
    WHITE,
)
from ..utils.types import ClassVar
from .entities.reinforcements import Reinforcement
from .slots import Slot
from .turrets.towers import Tower


# Define Button class
class Button(Sprite):
    """`Button` object represents a UI button sprite.

    Inherited from `Sprite`.

    Implements the functionality of a UI button sprite.
    """

    # Define class constants
    DISABLED_ALPHA = 100
    ENABLED_ALPHA = 255
    HEIGHT_RATIO = 3

    # Define class attributes expected to be assigned
    selected: ClassVar[Sprite | None] = None
    coin: ClassVar[int] = MINIMUM_COIN

    def __init__(
        self,
        filename: str,
        position: Vector,
        entity: type[Tower | Reinforcement],
    ) -> None:
        """Initialise a `Button` sprite object.

        Args:
            filename (str): The file of sprite.
            position (Vector): The position of sprite.
            entity (type[Tower | Reinforcement]): The game sprite class
            type stored in the button sprite.
        """

        # Initialised parent class
        super().__init__(filename, position)

        # Define attributes of button
        self.entity: type[Tower | Reinforcement] = entity
        self.timer: Timer | None = (
            Timer(self.clock, entity.COOLDOWN, initialise=False)
            if issubclass(entity, Reinforcement)
            else None
        )

    @classmethod
    def update_data(cls, coin: int, selected: Sprite | None) -> None:
        """Update the button class variable informations.

        Args:
            coin (int): The available coin of the player.
            selected (Sprite | None): The current cursor selection.
        """

        cls.coin = coin
        cls.selected = selected

    def tower_enabled(self) -> bool:
        """Determine if the button
        is a tower button and is enabled.

        Returns:
            bool: Whether the button is enabled.
        """

        return (
            issubclass(self.entity, Tower)
            and self.entity.affordable(self.coin)
            and isinstance(self.selected, Slot)
            and self.selected.tower is None
        )

    def reinforcement_enabled(self) -> bool:
        """Determine if the button
        is a reinforcement button and is enabled.

        Returns:
            bool: Whether the button is enabled.
        """

        return (
            issubclass(self.entity, Reinforcement)
            and self.entity.affordable(self.coin)
            and self.timer is not None
            and self.timer.available()
        )

    def on_click(self) -> int:
        """Event function called when the button is clicked.

        Returns:
            int: Return the cost for clicking the button.
        """

        # The side effect action if button is a tower button
        if (
            issubclass(self.entity, Tower)
            and self.tower_enabled()
            and isinstance(self.selected, Slot)
        ):
            self.selected.tower = self.entity(self.selected.xy)
            return self.entity.PRICE

        # The side effect action if button is a reinforcement button
        if (
            issubclass(self.entity, Reinforcement)
            and self.reinforcement_enabled()
            and self.timer
        ):
            self.entity()
            self.timer.update()
            return self.entity.PRICE

        return MINIMUM_COIN

    def on_hover_draw(self) -> None:
        """Event called when button is hovered."""

        # Validation of current game state
        if (
            not issubclass(self.entity, Tower)
            or not self.tower_enabled()
            or not isinstance(self.selected, Slot)
        ):
            return

        # Draw ghost overlay of tower
        arcade.draw_scaled_texture_rectangle(
            *self.selected.xy.convert(),
            texture=arcade.load_texture(self.entity.FILENAME),
        )

        # Draw the range overlay of tower
        arcade.draw_circle_filled(
            *self.selected.xy.convert(),
            radius=self.entity.RANGE,
            color=TRANSPARENT_LIGHT,
        )

    def on_draw(self) -> None:
        """Event called when button is to be drawn."""

        # Draw the price of the button's entity
        arcade.draw_text(
            f"${self.entity.PRICE}",
            self.x,
            self.y - self.height // self.HEIGHT_RATIO,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def update(self) -> None:
        """The update functionality for button class."""

        # Determine whether the button is active
        result: bool = self.tower_enabled() or self.reinforcement_enabled()

        # Change button opacity based on `result`
        self.alpha = self.ENABLED_ALPHA if result else self.DISABLED_ALPHA
