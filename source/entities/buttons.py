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
    TRANSPARENT_LIGHT,
    WHITE,
)
from ..utils.types import ClassVar
from .entities.reinforcements import Reinforcement
from .slots import Slot
from .turrets.towers import Tower


class Button(Sprite):
    DISABLED_ALPHA = 100
    ENABLED_ALPHA = 255

    selected: ClassVar[Sprite | None] = None
    coin: ClassVar[int] = 0

    def __init__(
        self,
        filename: str,
        position: Vector,
        entity: type[Tower | Reinforcement],
    ) -> None:
        super().__init__(filename, position)

        self.entity: type[Tower | Reinforcement] = entity
        self.timer: Timer | None = (
            Timer(self.clock, entity.COOLDOWN, initialise=False)
            if issubclass(entity, Reinforcement)
            else None
        )

    @classmethod
    def update_data(cls, coin: int, selected: Sprite | None) -> None:
        cls.coin = coin
        cls.selected = selected

    def tower_enabled(self) -> bool:
        return (
            issubclass(self.entity, Tower)
            and self.entity.affordable(self.coin)
            and isinstance(self.selected, Slot)
            and self.selected.tower is None
        )

    def reinforcement_enabled(self) -> bool:
        return (
            issubclass(self.entity, Reinforcement)
            and self.entity.affordable(self.coin)
            and self.timer is not None
            and self.timer.available()
        )

    def on_click(self) -> int:
        if (
            issubclass(self.entity, Tower)
            and self.tower_enabled()
            and isinstance(self.selected, Slot)
        ):
            self.selected.tower = self.entity(self.selected.xy)
            return self.entity.PRICE

        if (
            issubclass(self.entity, Reinforcement)
            and self.reinforcement_enabled()
            and self.timer
        ):
            self.entity()
            self.timer.update()
            return self.entity.PRICE

        return 0

    def on_hover_draw(self) -> None:
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

        # Draw the range of tower
        arcade.draw_circle_filled(
            *self.selected.xy.convert(),
            radius=self.entity.RANGE,
            color=TRANSPARENT_LIGHT,
        )

    def on_draw(self) -> None:
        arcade.draw_text(
            self.entity.PRICE,
            self.x,
            self.y - self.height // 3,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def update(self) -> None:
        result: bool = self.tower_enabled() or self.reinforcement_enabled()

        self.alpha = self.ENABLED_ALPHA if result else self.DISABLED_ALPHA
