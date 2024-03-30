# /entities/turrets/towers.py


import arcade

from ...utils import Vector
from ...utils.constants import TILE_SIZE
from ...utils.types import ClassVar, final
from .. import particles
from .turrets import Turret


class Tower(Turret):
    sprite_list: ClassVar[arcade.SpriteList]
    targets: ClassVar[arcade.SpriteList]

    FILENAME: ClassVar[str]
    FIRERATE: ClassVar[int]
    DAMAGE: ClassVar[int]
    RANGE: ClassVar[float]
    PRICE: ClassVar[int]

    def __init__(self, position: Vector) -> None:
        super().__init__(
            position=position,
            filename=self.FILENAME,
            firerate=self.FIRERATE,
            damage=self.DAMAGE,
            range=self.RANGE,
            targets=self.targets,
        )

        self.sprite_list.append(self)

    @classmethod
    def affordable(cls, amount: int) -> bool:
        return amount >= cls.PRICE

    def on_sell(self) -> int:
        self.kill()
        return self.PRICE // 2

    def attack(self) -> None:
        if not self.target:
            return

        super().attack()
        position: Vector = self.xy - (
            self.xy - self.target.xy
        ).normalise() * (self.height // 1.5)
        particles.flames.BigFlame(
            position,
            self.angle,
            min(self.FIRERATE // 2, 200),
        )


@final
class Canon(Tower):
    FILENAME = "./assets/Entities/Towers/Canon.png"
    FIRERATE = 2000
    DAMAGE = 20
    RANGE = 4 * TILE_SIZE
    PRICE = 35


@final
class MachineGun(Tower):
    FILENAME = "./assets/Entities/Towers/Gun.png"
    FIRERATE = 150
    DAMAGE = 1
    RANGE = 3 * TILE_SIZE
    PRICE = 20


@final
class RocketLauncher(Tower):
    FILENAME = "./assets/Entities/Towers/Rocket.png"
    FIRERATE = 3500
    DAMAGE = 15
    RANGE = 4 * TILE_SIZE
    PRICE = 60

    def attack(self) -> None:
        if not self.target:
            return

        particles.rockets.Rocket(
            self.xy,
            self.target.xy,
            targets=self.targets,
            damage=self.DAMAGE,
        )
