# /entities/entities/reinforcements.py


import arcade

from ...utils import Vector
from ...utils.types import ClassVar, final
from .. import turrets
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
            waypoints=self.waypoints,
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

        if self.is_end():
            self.on_die()


@final
class ArmourCar(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 50
    SPEED = 1


@final
class Tank(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 80
    SPEED = 1

    FIRERATE = 10
    DAMAGE = 10
    RANGE = 500

    def __init__(self) -> None:
        super().__init__()

        self.turret: turrets.canons.TankCanon = turrets.canons.TankCanon(
            filename="./assets/Entities/Vehicles/TankSmallGun.png",
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
