# /entities/entities/enemies.py


import arcade

from ...utils import Vector
from ...utils.types import ClassVar, NamedTuple, final
from .. import particles, turrets
from .entities import Entity


class Drops(NamedTuple):
    coin: type[particles.coins.Coin]
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
    HEALTH = 10
    SPEED = 2
    DROPS = Drops(particles.coins.Bronze, 1)


@final
class Zombie(Enemy):
    FILENAME = "./assets/Entities/Troops/Zombie.png"
    HEALTH = 8
    SPEED = 3
    DROPS = Drops(particles.coins.Bronze, 2)


@final
class Knight(Enemy):
    FILENAME = "./assets/Entities/Troops/Knight.png"
    HEALTH = 50
    SPEED = 1
    DROPS = Drops(particles.coins.Gold, 1)


@final
class Robot(Enemy):
    FILENAME = "./assets/Entities/Troops/Robot.png"
    HEALTH = 35
    SPEED = 2
    DROPS = Drops(particles.coins.Gold, 2)


@final
class Tank(Enemy):
    FILENAME = "./assets/Entities/Vehicles/TankBig.png"
    HEALTH = 250
    SPEED = 1
    DROPS = Drops(particles.coins.Gold, 5)

    FIRERATE = 2500
    DAMAGE = 25
    RANGE = 4 * 64

    def __init__(self) -> None:
        super().__init__()

        self.turret: turrets.canons.TankCanon = turrets.canons.TankCanon(
            filename="./assets/Entities/Vehicles/TankBigGun.png",
            position=self.xy,
            firerate=self.FIRERATE,
            damage=self.DAMAGE,
            range=self.RANGE,
            targets=self.targets,
        )
        self.sprite_list.append(self.turret)
        self.turret.face_point(self.movement.target.convert())

    def update(self) -> None:
        super().update()
        self.turret.xy = self.xy

        self.turret.update()
        if not self.turret.target and self.turret.reload.available():
            self.turret.face_point(self.movement.target.convert())

    def on_hover_draw(self) -> None:
        arcade.draw_circle_filled(
            *self.xy.convert(), radius=self.RANGE, color=(0, 0, 0, 50)
        )
        super().on_hover_draw()

    def on_die(self) -> None:
        self.turret.kill()
        super().on_die()
