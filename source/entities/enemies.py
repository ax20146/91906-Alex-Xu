# /entities/enemies.py


from ..utils import Movement, Sprite, Vector
from ..utils.types import ClassVar, NamedTuple, final
from .coins import *

__all__: list[str] = [
    "Enemy",
    "Solider",
    "Zombie",
    "Knight",
    "Robot",
    "Truck",
]


class Drops(NamedTuple):
    coin: type[Coin]
    amount: int


class Enemy(Sprite):
    waypoints: ClassVar[tuple[Vector, ...]]

    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[int]
    DROPS: ClassVar[Drops]

    def __init__(self) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=self.waypoints[0],
        )

        self.target: int = 1
        self.health: int = self.HEALTH
        self.movement: Movement = Movement(
            self, self.SPEED, self.waypoints[self.target]
        )

    def can_attack(self) -> bool:
        return self.target >= len(self.waypoints)

    def is_alive(self) -> bool:
        return self.health > 0

    def toward_target(self) -> None:
        self.face_point(self.waypoints[self.target].convert())

    def update_target(self) -> None:
        if self.position == self.waypoints[self.target]:
            self.target += 1
            self.movement.update_target(self.waypoints[self.target])

    def on_update(self, delta_time: float) -> None:
        self.movement.move(delta_time)
        self.toward_target()
        self.update_target()

        if not self.is_alive():
            self.die()

    def die(self) -> None:
        self.kill()

        for _ in range(self.DROPS.amount):
            self.DROPS.coin(self.position)


@final
class Solider(Enemy):
    FILENAME = "./assets/Entities/Troops/Soldier.png"
    HEALTH = 10
    SPEED = 80
    DROPS = Drops(Bronze, 2)


@final
class Zombie(Enemy):
    FILENAME = "./assets/Entities/Troops/Zombie.png"
    HEALTH = 10
    SPEED = 80
    DROPS = Drops(Bronze, 2)


@final
class Knight(Enemy):
    FILENAME = "./assets/Entities/Troops/Knight.png"
    HEALTH = 10
    SPEED = 80
    DROPS = Drops(Bronze, 2)


@final
class Robot(Enemy):
    FILENAME = "./assets/Entities/Troops/Robot.png"
    HEALTH = 10
    SPEED = 80
    DROPS = Drops(Bronze, 2)


@final
class Truck(Enemy):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 10
    SPEED = 80
    DROPS = Drops(Bronze, 2)
