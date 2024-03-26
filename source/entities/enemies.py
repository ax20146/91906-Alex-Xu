# /entities/enemies.py


import arcade

from ..utils import Sprite, Vector
from ..utils.constants import (
    ENEMY_KNIGHT_HEALTH,
    ENEMY_KNIGHT_SPEED,
    ENEMY_ROBOT_HEALTH,
    ENEMY_ROBOT_SPEED,
    ENEMY_SOLDIER_HEALTH,
    ENEMY_SOLDIER_SPEED,
    ENEMY_TRUCK_HEALTH,
    ENEMY_TRUCK_SPEED,
    ENEMY_ZOMBIE_HEALTH,
    ENEMY_ZOMBIE_SPEED,
)
from ..utils.types import ClassVar, TypeAlias, final
from .coins import *

CoinData = tuple[Coins, int]


class Enemy(Sprite):
    waypoints: ClassVar[tuple[Vector, ...]]

    def __init__(
        self, filename: str, *, speed: int, health: int, coin: CoinData
    ) -> None:
        super().__init__(
            filename,
            position=self.waypoints[0],
        )

        self.target: int = 1
        self.speed: int = speed
        self.health: int = health
        self.max_health: int
        self.name: str
        self.coin: CoinData = coin

    def can_attack(self) -> bool:
        return self.target >= len(self.waypoints)

    def move(self, dt: float) -> None:
        movement: Vector = self.waypoints[self.target] - self.position

        if movement.length() < self.speed * dt:
            self.position_update(movement)
            return

        self.position_update(movement.normalise() * self.speed * dt)

    def toward_target(self):
        self.face_point(self.waypoints[self.target].convert())

    def update_target(self) -> None:
        if self.position == self.waypoints[self.target]:
            self.target += 1

    def on_update(self, dt: float) -> None:
        if self.health <= 0:
            self.kill()
            return self.on_die()

        self.move(dt)
        self.toward_target()
        self.update_target()

    def on_select_draw(self) -> None:
        self.draw_hit_box(line_thickness=2)
        arcade.draw_text(
            f"{self.health}/{self.max_health}",
            self.x,
            self.y + 25,
            anchor_x="center",
            anchor_y="center",
        )

    def on_die(self) -> None:
        for _ in range(self.coin[1]):
            self.coin[0](self.position)


@final
class Solider(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entities/Troops/Solider.png",
            speed=ENEMY_SOLDIER_SPEED,
            health=ENEMY_SOLDIER_HEALTH,
            coin=(Bronze, 2),
        )


@final
class Zombie(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entities/Troops/Zombie.png",
            speed=ENEMY_ZOMBIE_SPEED,
            health=ENEMY_ZOMBIE_HEALTH,
            coin=(Bronze, 4),
        )


@final
class Knight(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entities/Troops/Knight.png",
            speed=ENEMY_KNIGHT_SPEED,
            health=ENEMY_KNIGHT_HEALTH,
            coin=(Bronze, 4),
        )


@final
class Robot(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entities/Troops/Robot.png",
            speed=ENEMY_ROBOT_SPEED,
            health=ENEMY_ROBOT_HEALTH,
            coin=(Silver, 1),
        )


@final
class Truck(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entities/Vehicles/TankSmall.png",
            speed=ENEMY_TRUCK_SPEED,
            health=ENEMY_TRUCK_HEALTH,
            coin=(Gold, 1),
        )


Enemies: TypeAlias = type[Solider | Zombie | Knight | Robot | Truck]
