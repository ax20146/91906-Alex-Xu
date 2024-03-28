# /entities/turrets/towers.py


import arcade

from ...utils import Vector
from ...utils.constants import TILE_SIZE
from ...utils.types import ClassVar, final
from ..particles.flames import BigFlame
from ..particles.rockets import Rocket
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

    def attack(self) -> None:
        if not self.target:
            return

        super().attack()
        BigFlame(
            (self.xy - self.target.xy).normalise() * (self.height // 1.2),
            self.angle,
            min(self.FIRERATE // 2, 200),
        )


@final
class Canon(Tower):
    FILENAME = "./assets/Entities/Towers/Canon.png"
    FIRERATE = 1500
    DAMAGE = 10
    RANGE = 3.5 * TILE_SIZE
    PRICE = 10


@final
class MachineGun(Tower):
    FILENAME = "./assets/Entities/Towers/Gun.png"
    FIRERATE = 150
    DAMAGE = 1
    RANGE = 2 * TILE_SIZE
    PRICE = 10


@final
class RocketLauncher(Tower):
    FILENAME = "./assets/Entities/Towers/Rocket.png"
    FIRERATE = 3000
    DAMAGE = 20
    RANGE = 4 * TILE_SIZE
    PRICE = 10

    def attack(self) -> None:
        if not self.target:
            return

        Rocket(
            self.xy,
            self.target.xy,
            targets=self.targets,
            damage=self.DAMAGE,
        )
