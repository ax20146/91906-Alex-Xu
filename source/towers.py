from math import atan2, cos, sin
from typing import final

import arcade

from .enemies import Enemy
from .entities import TurretEntity
from .flames import BigFlame
from .utils import ClassSpriteList, Point, Sprite, TuplePoint
from .utils.constants import Damage, Duration, Price, Range


class Tower(TurretEntity):
    lst: ClassSpriteList

    def __init__(
        self,
        filename: str,
        *,
        position: tuple[float, float],
        damage: int,
        range: int,
        cooldown: int,
        price: int,
    ) -> None:
        super().__init__(
            filename,
            position,
            damage=damage,
            range=range,
            cooldown=cooldown,
        )

        self.lst.append(self)
        self.price: int = price

    def attack(self) -> None:
        self.target.health -= self.damage


@final
class Canon(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Canon.png",
            position=position,
            damage=Damage.HIGH,
            range=Range.FAR,
            cooldown=Duration.LONG,
            price=Price.MEDIUM,
        )

    def attack(self) -> None:
        super().attack()
        BigFlame(self.angle, self.position, delay=Duration.SHORTER)


@final
class MachineGun(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Gun.png",
            position=position,
            damage=Damage.LOW,
            range=Range.SHORT,
            cooldown=Duration.SHORTER,
            price=Price.LOW,
        )

    def attack(self) -> None:
        super().attack()
        BigFlame(self.angle, self.position, delay=Duration.SHORTEST)


class Rocket(Sprite):
    lst: ClassSpriteList
    targets: ClassSpriteList

    def __init__(
        self,
        rotation: float,
        position: TuplePoint,
        *,
        target: TuplePoint,
        damage: int,
    ) -> None:
        super().__init__("./assets/Particles/Rocket.png", rotation, position)

        self.lst.append(self)
        self.target: Point = Point(*target)
        self.speed: int = 350
        self.damage: int = damage

    def move(self, dt: float) -> None:
        position: Point = Point(*self.position)
        target: Point = self.target

        angle: float = -atan2(target.x - position.x, target.y - position.y)

        self.center_x -= self.speed * sin(angle) * dt
        self.center_y += self.speed * cos(angle) * dt

    def toward_target(self):
        self.face_point(self.target.convert())

    def reached_target(self):
        position: Point = Point(*self.position)

        if position.within(self.target, range=3):
            self.attack()
            self.kill()

    def attack(self):
        targets = (
            sprite
            for sprite in self.targets
            if arcade.get_distance_between_sprites(self, sprite) <= 50
        )

        target: Enemy
        for target in targets:  # type: ignore
            print(target)
            target.health -= self.damage

    def on_update(self, dt: float) -> None:
        self.move(dt)
        self.toward_target()
        self.reached_target()


@final
class RocketLauncher(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Rocket.png",
            position=position,
            damage=400,
            range=Range.SHORT,
            cooldown=2500,
            price=100,
        )

    def attack(self) -> None:
        Rocket(
            self.angle,
            self.position,
            target=self.target.position,
            damage=self.damage,
        )


Towers = type[Canon | MachineGun | RocketLauncher]
