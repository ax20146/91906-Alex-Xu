# /entities/entities/reinforcements.py


import arcade

from ...utils import Vector
from ...utils.types import ClassVar, final
from .enemies import Enemy
from .entities import Entity


class Reinforcement(Entity):
    waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]

    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[float]

    def __init__(self) -> None:
        super().__init__(
            filename=self.FILENAME,
            health=self.HEALTH,
            speed=self.SPEED,
        )

    def on_collide(self) -> None:
        if not (
            sprites := arcade.check_for_collision_with_list(
                self, self.targets
            )
        ):
            return

        sprite: arcade.Sprite = sprites[0]
        if not isinstance(sprite, Enemy):
            return

        damage: int = sprite.health
        sprite.health -= self.health
        self.health -= damage

    def update(self) -> None:
        super().update()
        self.on_collide()

        if self.is_end() or self.is_dead():
            self.kill()


@final
class ArmourCar(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 50
    SPEED = 1


@final
class Tank(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 75
    SPEED = 0.5

    def __init__(self) -> None:
        super().__init__()

        self.turret = ...

    def update(self) -> None:
        return super().update()
        self.turret
