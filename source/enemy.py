from typing import ClassVar

import arcade

from .coins import Gold
from .entity import PathEntity
from .utils import Health, Speed


class Enemy(PathEntity):
    coin_list: ClassVar[arcade.SpriteList]
    health: int

    def on_die(self) -> None:
        self.kill()
        self.coin_list.append(Gold((self.center_x, self.center_y)))

    def on_end(self) -> None:
        self.kill()
        Enemy.health -= 1


class Soldier(Enemy):
    def __init__(self) -> None:
        super().__init__(
            filename="./assets/Entity/Troops/Soldier.png",
            speed=Speed.MEDIUM.value,
            health=Health.LOW.value,
        )


class Robot(Enemy):
    def __init__(self) -> None:
        super().__init__(
            filename="./assets/Entity/Troops/Robot.png",
            speed=Speed.MEDIUM.value,
            health=Health.HIGH.value,
        )


class Truck(Enemy):
    def __init__(self) -> None:
        super().__init__(
            filename="./assets/Entity/Tanks/TankSmall.png",
            speed=Speed.FAST.value,
            health=Health.HIGH.value,
        )


class Zombie(Enemy):
    def __init__(self) -> None:
        super().__init__(
            filename="./assets/Entity/Troops/Zombie.png",
            speed=Speed.FAST.value,
            health=Health.LOW.value,
        )


class Knight(Enemy):
    def __init__(self) -> None:
        super().__init__(
            filename="./assets/Entity/Troops/Knight.png",
            speed=Speed.SLOW.value,
            health=Health.HIGH.value,
        )
