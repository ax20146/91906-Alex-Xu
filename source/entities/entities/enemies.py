# /entities/entities/enemies.py


import arcade

from ...utils import Vector
from ...utils.types import ClassVar, NamedTuple, final
from ..particles.coins import Bronze, Coin, Gold
from ..turrets import canons
from .entities import Entity


class Drops(NamedTuple):
    coin: type[Coin]
    amount: int


class Enemy(Entity):
    sprite_list: ClassVar[arcade.SpriteList]
    waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]

    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[float]
    DROPS: ClassVar[Drops]

    def __init__(self) -> None:
        super().__init__(
            filename=self.FILENAME,
            health=self.HEALTH,
            speed=self.SPEED,
            waypoints=self.waypoints,
        )

        self.sprite_list.append(self)

    def on_end(self) -> int:
        self.on_die()
        return self.health

    def on_die(self) -> None:
        super().on_die()

        for _ in range(self.DROPS.amount):
            self.DROPS.coin(self.xy)


@final
class Soldier(Enemy):
    FILENAME = "./assets/Entities/Troops/Soldier.png"
    HEALTH = 20
    SPEED = 1
    DROPS = Drops(Bronze, 2)


@final
class Zombie(Enemy):
    FILENAME = "./assets/Entities/Troops/Zombie.png"
    HEALTH = 10
    SPEED = 2
    DROPS = Drops(Bronze, 3)


@final
class Knight(Enemy):
    FILENAME = "./assets/Entities/Troops/Knight.png"
    HEALTH = 40
    SPEED = 0.5
    DROPS = Drops(Gold, 1)


@final
class Robot(Enemy):
    FILENAME = "./assets/Entities/Troops/Robot.png"
    HEALTH = 30
    SPEED = 1
    DROPS = Drops(Gold, 2)


@final
class Tank(Enemy):
    FILENAME = "./assets/Entities/Vehicles/TankBig.png"
    HEALTH = 200
    SPEED = 1
    DROPS = Drops(Gold, 5)

    FIRERATE = 1000
    DAMAGE = 10
    RANGE = 800

    def __init__(self) -> None:
        super().__init__()

        self.turret: canons.TankCanon = canons.TankCanon(
            filename="./assets/Entities/Vehicles/TankBigGun.png",
            position=self.xy,
            firerate=self.FIRERATE,
            damage=self.DAMAGE,
            range=self.RANGE,
            targets=self.targets,
        )
        self.sprite_list.append(self.turret)

    def update(self) -> None:
        super().update()
        self.turret.xy = self.xy

        self.turret.update()
        if not self.turret.target:
            self.turret.face_point(self.movement.target.convert())

    def on_die(self) -> None:
        self.turret.kill()
        super().on_die()
