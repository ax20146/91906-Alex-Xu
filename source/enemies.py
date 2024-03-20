from typing import final

from .coins import Bronze, Coins, Gold
from .entities import PathEntity
from .utils.constants import Health, Speed


class Enemy(PathEntity):
    health: int

    def __init__(
        self,
        filename: str,
        *,
        speed: int,
        health: int,
        coin: tuple[Coins, int]
    ) -> None:
        super().__init__(
            filename,
            speed=speed,
            health=health,
        )
        self.coin: tuple[Coins, int] = coin

    def on_die(self) -> None:
        for _ in range(self.coin[1]):
            self.coin[0](self.position)

    def on_end(self) -> None:
        Enemy.health -= 1


@final
class Soldier(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Troops/Soldier.png",
            speed=Speed.MEDIUM,
            health=Health.MEDIUM,
            coin=(Bronze, 1),
        )


@final
class Zombie(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Troops/Zombie.png",
            speed=Speed.FAST,
            health=Health.LOW,
            coin=(Bronze, 2),
        )


@final
class Knight(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Troops/Knight.png",
            speed=Speed.SLOW,
            health=Health.HIGH,
            coin=(Bronze, 2),
        )


@final
class Robot(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Troops/Robot.png",
            speed=Speed.FAST,
            health=Health.MEDIUM,
            coin=(Bronze, 3),
        )


@final
class Truck(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Tanks/TankSmall.png",
            speed=Speed.MEDIUM,
            health=Health.HIGH,
            coin=(Gold, 1),
        )
