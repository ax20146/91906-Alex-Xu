# /entities/entities/entities.py


import arcade

from ...utils import Movement, Sprite, Vector
from ...utils.constants import (
    STAT_UI_HEIGHT,
    STAT_UI_MARGIN,
    STAT_UI_OFFSET_LARGE,
    STAT_UI_OFFSET_SMALL,
    STAT_UI_WIDTH,
    UI_BACKGROUND_COLOUR,
    UI_HEALTHBAR_COLOUR,
)
from ...utils.functions import process_pascal_case

FONT = "Kenney Future Narrow"


class Entity(Sprite):
    def __init__(
        self,
        *,
        filename: str,
        health: int,
        speed: float,
        waypoints: tuple[Vector, ...],
    ) -> None:
        super().__init__(
            filename=filename,
            position=self.waypoints[0],
        )

        self.target: int = 1
        self.health: int = health
        self.HEALTH: int = health
        self.waypoints = waypoints
        self.movement: Movement = Movement(
            self, self.waypoints[self.target], speed
        )

    def is_end(self) -> bool:
        return self.target >= len(self.waypoints)

    def is_dead(self) -> bool:
        return self.health <= 0

    def distance(self) -> float:
        return (self.xy - self.waypoints[self.target]).length()

    def on_hover_draw(self) -> None:
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET_SMALL,
            STAT_UI_WIDTH + STAT_UI_MARGIN,
            STAT_UI_HEIGHT + STAT_UI_MARGIN,
            UI_BACKGROUND_COLOUR,
        )
        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET_SMALL,
            max(self.health, 0) / self.HEALTH * STAT_UI_WIDTH,
            STAT_UI_HEIGHT,
            UI_HEALTHBAR_COLOUR,
        )

        arcade.draw_rectangle_filled(
            self.x,
            self.y + STAT_UI_OFFSET_LARGE,
            STAT_UI_WIDTH + STAT_UI_MARGIN,
            (STAT_UI_HEIGHT + STAT_UI_MARGIN) * 3,
            UI_BACKGROUND_COLOUR,
        )
        arcade.draw_text(
            f"{process_pascal_case(self.__class__.__name__)}:",
            self.x - STAT_UI_WIDTH // 2,
            self.y + STAT_UI_OFFSET_LARGE + 2,
            font_name=FONT,
            font_size=8,
            anchor_x="left",
            anchor_y="center",
        )
        arcade.draw_text(
            f"{max(self.health, 0)} / {self.HEALTH}",
            self.x + STAT_UI_WIDTH // 2,
            self.y + STAT_UI_OFFSET_LARGE + 2,
            font_name=FONT,
            font_size=8,
            anchor_x="right",
            anchor_y="center",
        )

        self.draw_hit_box(line_thickness=2)

    def on_die(self) -> None:
        self.kill()

    def update(self) -> None:
        self.movement.update()
        self.update_target()

        if self.is_dead():
            self.on_die()

    def update_target(self) -> None:
        if self.xy == self.waypoints[self.target]:
            self.target += 1

        if not self.is_end():
            self.movement.update_target(self.waypoints[self.target])
