# /entities/particles/coins.py


import arcade

from ...utils import Vector
from ...utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from ...utils.types import ClassVar, final
from .particles import Particle


class Coin(Particle):
    LIFETIME = 8000
    sprite_list: ClassVar[arcade.SpriteList]

    FILENAME: ClassVar[str]
    VALUE: ClassVar[int]

    def __init__(self, position: Vector) -> None:
        super().__init__(
            filename=self.FILENAME,
            duration=self.LIFETIME,
            position=position.randomise(TILE_SIZE).limit(
                Vector(0, 0), Vector(SCREEN_WIDTH, SCREEN_HEIGHT)
            ),
        )

    def on_collect(self) -> int:
        self.kill()
        return self.VALUE


@final
class Gold(Coin):
    FILENAME = "./assets/Entities/Coins/Gold.png"
    VALUE = 5


@final
class Bronze(Coin):
    FILENAME = "./assets/Entities/Coins/Bronze.png"
    VALUE = 1
