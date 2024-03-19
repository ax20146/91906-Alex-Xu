# /turret.py


from abc import ABC, abstractmethod
from typing import ClassVar

import arcade

from .enemy import Enemy
from .particle import Fire
from .utils import Sprite, VectorTuple


class Turret(Sprite, ABC):
    targets: ClassVar[arcade.SpriteList]
    particles: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        filename: str,
        position: VectorTuple,
        damage: int,
        range: int,
        cooldown: int,
    ) -> None:
        super().__init__(
            filename=filename,
            position=position,
        )

        self.damage: int = damage
        self.range: int = range

        self.last_attack: float = 0
        self.cooldown: int = cooldown

        self.target: Enemy

    def can_attack(self) -> bool:
        return self.clock.now() - self.last_attack >= self.cooldown

    def select_target(self) -> Enemy | None:
        if (data := arcade.get_closest_sprite(self, self.targets)) is None:
            return

        sprite, distance = data
        if not isinstance(sprite, Enemy) or distance > self.range:
            return

        return sprite

    def on_update(self, dt: float) -> None:
        if (target := self.select_target()) is None:
            return

        self.target = target

        self.face_point(self.target.position)

        if self.can_attack():
            self.attack()
            self.last_attack = self.clock.now()

    @abstractmethod
    def attack(self) -> None:
        raise NotImplementedError


class Canon(Turret):
    def __init__(self, position: VectorTuple) -> None:
        super().__init__(
            "./assets/towers/canon.png",
            position,
            damage=50,
            range=5 * 64,
            cooldown=1000,
        )

    def attack(self) -> None:
        self.target.health -= self.damage

        self.particles.append(
            Fire(self.angle, (self.center_x, self.center_y))
        )
