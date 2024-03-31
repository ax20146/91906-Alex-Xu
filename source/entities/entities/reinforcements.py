# /entities/entities/reinforcements.py


import arcade

from ...utils import Timer, Vector
from ...utils.types import ClassVar, final
from .. import turrets
from .enemies import Enemy
from .entities import Entity


class Reinforcement(Entity):
    sprite_list: ClassVar[arcade.SpriteList]
    waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]
    timer = None

    FILENAME: ClassVar[str]
    HEALTH: ClassVar[int]
    SPEED: ClassVar[float]
    PRICE: ClassVar[int]
    COOLDOWN: ClassVar[int]

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
        if not cls.timer:
            cls.timer = Timer(cls.clock, cls.COOLDOWN)
            cls.timer._previous = -cls.timer.duration

        return amount >= cls.PRICE and cls.timer.available()

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
            self.on_die()


@final
class Truck(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 40
    SPEED = 2
    PRICE = 35
    COOLDOWN = 5000


@final
class Tank(Reinforcement):
    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 75
    SPEED = 1
    PRICE = 75
    COOLDOWN = 10000

    FIRERATE = 2000
    DAMAGE = 10
    RANGE = 3.5 * 64

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
