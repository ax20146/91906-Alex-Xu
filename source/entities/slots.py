# /entities/slots.py


import arcade

from ..utils import Sprite, Vector
from ..utils.functions import process_pascal_case
from ..utils.types import final
from .turrets import towers


@final
class Slot(Sprite):
    def __init__(self, position: Vector) -> None:
        super().__init__(
            filename="./assets/Entities/Slot.png",
            position=position,
        )

        self.turret: towers.Tower | None = None

    def on_hover_draw(self) -> None:
        name: str = (
            process_pascal_case(self.turret.__class__.__name__)
            if self.turret
            else "Slot"
        )

        arcade.draw_text(
            name,
            self.x,
            self.y + 35,
            font_size=8,
            color=(50, 50, 50),
            anchor_x="center",
            anchor_y="center",
        )

        self.draw_hit_box((50, 50, 50), line_thickness=2)

    def on_select_draw(self) -> None: ...
