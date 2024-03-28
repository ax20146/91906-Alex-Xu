# /entities/entities/entities.py


import arcade

from ...utils import Movement, Sprite, Vector
from ...utils.types import ClassVar


class Entity(Sprite):
    waypoints: ClassVar[tuple[Vector, ...]]

    def __init__(
        self,
        *,
        filename: str,
        health: int,
        speed: float,
    ) -> None:
        super().__init__(
            filename=filename,
            position=self.waypoints[0],
        )

        self.target: int = 1
        self.health: int = health
        self.HEALTH: int = health
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
            self.y + 35,
            82,
            5,
            (0, 0, 0, 180),
        )
        arcade.draw_rectangle_filled(
            self.x,
            self.y + 35,
            self.health / self.HEALTH * 80,
            3,
            (79, 189, 101, 255),
        )

        arcade.draw_rectangle_filled(
            self.x, self.y + 48, 82, 15, (0, 0, 0, 180)
        )
        arcade.draw_text(
            f"{self.__class__.__name__.capitalize()}:",
            self.x - 40,
            self.y + 50,
            font_size=8,
            bold=True,
            anchor_x="left",
            anchor_y="center",
        )
        arcade.draw_text(
            f"{self.health}/{self.HEALTH}",
            self.x + 40,
            self.y + 50,
            font_size=8,
            bold=True,
            anchor_x="right",
            anchor_y="center",
        )

        self.draw_hit_box(line_thickness=2)

    def update(self) -> None:
        self.movement.update()
        self.update_target()

    def update_target(self) -> None:
        if self.xy == self.waypoints[self.target]:
            self.target += 1

        if not self.is_end():
            self.movement.update_target(self.waypoints[self.target])
