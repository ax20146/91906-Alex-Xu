# /entities/coins.py


import arcade

from ..utils import Point, Sprite, Timer
from ..utils.constants import (
    COIN_BRONZE_VALUE,
    COIN_GOLD_VALUE,
    COIN_LIFETIME,
    COIN_SILVER_VALUE,
    TILE_SIZE,
)
from ..utils.functions import limit_within, randrange
from ..utils.types import ClassVar, TypeAlias, final


class Coin(Sprite):
    sprite_list: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        filename: str,
        *,
        position: Point,
        value: int,
    ) -> None:
        position = Point(
            randrange(position.x, TILE_SIZE),
            randrange(position.y, TILE_SIZE),
        )

        super().__init__(
            filename,
            position=limit_within(position),
        )

        self.value: int = value
        self.timer: Timer = Timer(self.clock, delay=COIN_LIFETIME)

        self.sprite_list.append(self)

    def on_collect(self, amount: int) -> int:
        self.kill()
        return amount + self.value

    def on_update(self, dt: float) -> None:
        if self.timer.available():
            self.kill()


@final
class Gold(Coin):
    def __init__(self, position: Point) -> None:
        super().__init__(
            "./assets/Entities/Coins/Gold.png",
            position=position,
            value=COIN_GOLD_VALUE,
        )


@final
class Silver(Coin):
    def __init__(self, position: Point) -> None:
        super().__init__(
            "./assets/Entities/Coins/Silver.png",
            position=position,
            value=COIN_SILVER_VALUE,
        )


@final
class Bronze(Coin):
    def __init__(self, position: Point) -> None:
        super().__init__(
            "./assets/Entities/Coins/Bronze.png",
            position=position,
            value=COIN_BRONZE_VALUE,
        )


Coins: TypeAlias = type[Gold | Silver | Bronze]
