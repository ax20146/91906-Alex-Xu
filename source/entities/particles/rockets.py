# /entities/particles/rockets.py


import arcade

from ...utils import Movement, Vector
from ...utils.constants import TILE_SIZE
from ...utils.types import Iterator, final
from ..entity import Entity
from .particles import Particle


@final
class Rocket(Particle):
    FILENAME = "./assets/Particles/Rocket.png"

    def __init__(
        self,
        position: Vector,
        target: Vector,
        *,
        targets: arcade.SpriteList,
        damage: int,
        range: int = TILE_SIZE // 2,
        speed: float = 8,
    ) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=position,
        )

        self.range: int = range
        self.damage: int = damage
        self.targets: arcade.SpriteList = targets
        self.movement: Movement = Movement(self, target, speed)

    def explode(self) -> None:
        sprites: Iterator[Entity] = (
            sprite
            for sprite in self.targets
            if isinstance(sprite, Entity)
            and arcade.get_distance_between_sprites(self, sprite)
            <= self.range
        )

        for target in sprites:
            target.health -= self.damage

    def update(self) -> None:
        self.movement.update()

        if self.xy == self.movement.target:
            self.explode()
            self.kill()
