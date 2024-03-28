# /entities/entities/reinforcements.py


import arcade

from ...utils import Vector
from ...utils.types import ClassVar, final
from ..turrets.canons import TankCanon
from .enemies import Enemy
from .entities import Entity


class Reinforcement(Entity):
    sprite_list: ClassVar[arcade.SpriteList]
    waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]

    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[float]
    PRICE: ClassVar[int]

    def __init__(self) -> None:
        super().__init__(
            filename=self.FILENAME,
            health=self.HEALTH,
            speed=self.SPEED,
        )

        self.sprite_list.append(self)

    @classmethod
    def affordable(cls, amount: int) -> bool:
        return amount >= cls.PRICE

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

    FIRERATE = 10
    DAMAGE = 10
    RANGE = 10

    def __init__(self) -> None:
        super().__init__()

        self.turret: TankCanon = TankCanon(
            filename="./assets/Entities/Vehicles/TankSmallGun.png",
            position=self.xy,
            firerate=self.FIRERATE,
            damage=self.DAMAGE,
            range=self.RANGE,
            targets=self.targets,
        )

    def update(self) -> None:
        super().update()
        self.turret.xy = self.xy

        if not self.turret.target:
            return

        self.turret.face_point(self.movement.target.convert())
