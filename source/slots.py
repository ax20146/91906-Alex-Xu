from typing import final

import arcade

from .towers import Tower
from .utils import Sprite, TuplePoint


@final
class Slot(Sprite):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Slot.png",
            position=position,
        )

        self.turret: Tower | None = None

    def on_select(self) -> None:
        if not self.turret:
            return None

        self.draw_hit_box(line_thickness=2)
        arcade.draw_circle_filled(
            *self.position, radius=self.turret.range, color=(0, 0, 0, 50)
        )
        arcade.draw_text(
            f"{self.turret.__class__.__name__.title()}\nDamage: {self.turret.damage}",
            self.x,
            self.y - 50,
            width=100,
            align="center",
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, dt: float) -> None:
        pass
