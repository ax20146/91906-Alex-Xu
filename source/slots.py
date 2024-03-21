from typing import final

import arcade

from .towers import Tower, Towers
from .utils import Sprite, TuplePoint


def entity_texture(
    entity: Towers, position: TuplePoint
) -> arcade.Texture | None:
    tower = entity(position)
    tower.kill()
    return tower.texture


@final
class Slot(Sprite):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Slot.png",
            position=position,
        )

        self.turret: Tower | None = None

    def on_select_draw(self) -> None:
        if not self.turret:
            return

        arcade.draw_texture_rectangle(
            self.x,
            self.y,
            width=256,
            height=128,
            texture=arcade.load_texture("./assets/Banner_Horizontal.png"),
        )
        arcade.draw_texture_rectangle(
            self.x - 64,
            self.y,
            width=64,
            height=64,
            texture=arcade.load_texture("./assets/Entity/Towers/Canon.png"),
        )

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
