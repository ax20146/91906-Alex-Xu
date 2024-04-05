# /entities/entities/entities.py
"""`Entities` module containing the `Entity` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils import Sprite, Vector
from ...utils.constants import (
    ANCHOR_CENTER,
    ANCHOR_LEFT,
    ANCHOR_RIGHT,
    BLACK,
    FONT,
    FONT_SMALL,
    HEALTHBAR_COLOUR,
    MINIMUM_HEALTH,
    STAT_UI_FULL_H,
    STAT_UI_FULL_W,
    STAT_UI_HALF_W,
    STAT_UI_HEIGHT,
    STAT_UI_LARGE_HEIGHT,
    STAT_UI_LARGE_OFFSET,
    STAT_UI_OFFSET,
    STAT_UI_OUTLINE,
    STAT_UI_WIDTH,
    TRANSPARENT_DARK,
    WHITE,
)
from ...utils.types import ClassVar


# Define Entity class
class Entity(Sprite):
    """`Entity` object represents a entity sprite.

    Inherited from `Sprite`.

    Implements the base functionality of a entity sprite.
    """

    # Define class attributes expected to be override
    waypoints: ClassVar[tuple[Vector, ...]]

    # Define class constants expected to be override
    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[float]

    def __init__(self) -> None:
        """Initialise a `Entity` sprite object."""

        # Initialised parent class
        super().__init__(self.FILENAME, self.waypoints[0], add=True)

        # Define attributes of entity
        self.target_idx: int = 1
        self.health: int = self.HEALTH

    def is_end(self) -> bool:
        """Determine whether the entity reached end of path.

        Returns:
            bool: Whether the entity reached end.
        """

        return self.target_idx >= len(self.waypoints)

    def is_dead(self) -> bool:
        """Determine whether the entity is dead.

        Returns:
            bool: Whether the entity is dead.
        """

        return self.health <= MINIMUM_HEALTH

    def distance(self) -> float:
        """Calculate the distance to the entity's target.

        Returns:
            float: The distance to its target.
        """

        return abs(self.xy - self.waypoints[self.target_idx])

    def on_die(self) -> None:
        """Event called when entity dies."""

        self.kill()

    def on_hover_draw(self) -> None:
        """Event called when entity is hovered."""

        # Draw the entity healthbar
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET,
            width=STAT_UI_FULL_W,
            height=STAT_UI_FULL_H,
            color=TRANSPARENT_DARK,
        )
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET,
            width=max(self.health, MINIMUM_HEALTH)
            / self.HEALTH
            * STAT_UI_WIDTH,
            height=STAT_UI_HEIGHT,
            color=HEALTHBAR_COLOUR,
        )

        # Draw the entity name & health information
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_LARGE_OFFSET,
            width=STAT_UI_FULL_W,
            height=STAT_UI_LARGE_HEIGHT,
            color=TRANSPARENT_DARK,
        )
        arcade.draw_text(
            f"{self.name()}:",
            self.x - STAT_UI_HALF_W,
            self.y + STAT_UI_LARGE_OFFSET,
            font_name=FONT,
            font_size=FONT_SMALL,
            anchor_x=ANCHOR_LEFT,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )
        arcade.draw_text(
            f"{max(self.health, MINIMUM_HEALTH)} / {self.HEALTH}",
            self.x + STAT_UI_HALF_W,
            self.y + STAT_UI_LARGE_OFFSET,
            font_name=FONT,
            font_size=FONT_SMALL,
            anchor_x=ANCHOR_RIGHT,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

        # Outline the entity
        self.draw_hit_box(BLACK, STAT_UI_OUTLINE)

    def on_select_draw(self) -> None:
        """Event called when entity is selected."""
        self.on_hover_draw()

    def update_target(self) -> None:
        """Update the entity target index."""

        if self.xy == self.waypoints[self.target_idx]:
            self.target_idx += 1

    def update(self) -> None:
        """The update functionality for entity class."""

        # Determine if entity should die
        if self.is_dead():
            return self.on_die()

        # Move, Rotate & Update the entity target
        self.rotate(self.waypoints[self.target_idx])
        self.move(self.waypoints[self.target_idx], self.SPEED)
        self.update_target()
