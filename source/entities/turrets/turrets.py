# /entities/turrets/turrets.py


import arcade

from ...utils import Sprite, Timer, Vector
from .. import entities


class Turret(Sprite):
    def __init__(
        self,
        *,
        filename: str,
        position: Vector,
        firerate: int,
        damage: int,
        range: float,
        targets: arcade.SpriteList
    ) -> None:
        super().__init__(
            filename=filename,
            position=position,
        )

        self.timer: Timer = Timer(self.clock, firerate)
        self.reload: Timer = Timer(self.clock, firerate // 3)

        self.targets: arcade.SpriteList = targets
        self.target: entities.Entity | None = None
        self.damage: int = damage
        self.range: float = range

    def update_target(self) -> None:
        self.target = None

        for sprite in (
            sprite
            for sprite in self.targets
            if isinstance(sprite, entities.Entity)
            and self.xy.within(sprite.xy, self.range)
        ):
            self.target = self.target or sprite

            condition: bool = sprite.target > self.target.target or (
                sprite.target == self.target.target
                and sprite.distance() < self.target.distance()
            )

            self.target = sprite if condition else self.target

    def update(self) -> None:
        self.update_target()
        if not self.reload.available() or not self.target:
            return

        self.face_point(self.target.xy.convert())
        if self.timer.available():
            self.attack()
            self.timer.update()
            self.reload.update()

    def attack(self) -> None:
        if not self.target:
            return
        self.target.health -= self.damage
