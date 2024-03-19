# Import Dependencies
from abc import ABC, abstractmethod
from typing import ClassVar

import arcade

from ..utils import Sprite, VectorTuple


class TurretEntity(Sprite, ABC):
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
            filename,
            position=position,
        )

        self.damage: int = damage
        self.range: int = range

        self.last_attack: float = 0
        self.cooldown: int = cooldown

        self.target: Sprite

    def can_attack(self) -> bool:
        return self.clock.now() - self.last_attack >= self.cooldown

    def select_target(self) -> Sprite | None:
        if (data := arcade.get_closest_sprite(self, self.targets)) is None:
            return

        sprite, distance = data
        if not isinstance(sprite, Sprite) or distance > self.range:
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
