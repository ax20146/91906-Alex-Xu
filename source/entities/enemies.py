# /entities/enemies.py

from ..utils.types import NamedTuple, final
from .coins import Bronze, Coin, Gold, Silver
from .entity import Entity


class Drops(NamedTuple):
    coin: type[Coin]
    amount: int


class Enemy(Entity):
    DROPS: Drops

    def on_end(self) -> int:
        self.on_die()
        return self.health

    def on_die(self) -> None:
        self.kill()

        for _ in range(self.DROPS.amount):
            self.DROPS.coin(self.xy)

    def update(self) -> None:
        super().update()

        if not self.is_alive():
            self.on_die()


@final
class Soldier(Enemy):
    FILENAME = "/assets/Entities/Troops/Soldier.png"
    HEALTH = 10
    SPEED = 10
    DROPS = Drops(Bronze, 3)


@final
class Zombie(Enemy):
    FILENAME = "/assets/Entities/Troops/Zombie.png"
    HEALTH = 5
    SPEED = 25
    DROPS = Drops(Bronze, 3)


@final
class Knight(Enemy):
    FILENAME = "/assets/Entities/Troops/Knight.png"
    HEALTH = 20
    SPEED = 8
    DROPS = Drops(Silver, 1)


@final
class Robot(Enemy):
    FILENAME = "/assets/Entities/Troops/Robot.png"
    HEALTH = 20
    SPEED = 10
    DROPS = Drops(Silver, 2)


@final
class Truck(Enemy):
    FILENAME = "/assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 40
    SPEED = 10
    DROPS = Drops(Gold, 1)
