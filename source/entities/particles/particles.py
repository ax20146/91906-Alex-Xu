# /entities/particles/particles.py


import arcade

from ...utils import Sprite, Timer, Vector
from ...utils.types import ClassVar


class Particle(Sprite):
    sprite_list: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        *,
        filename: str,
        position: Vector,
        rotation: float = 0,
        duration: int = 0,
    ) -> None:
        super().__init__(
            filename=filename,
            position=position,
            rotation=rotation,
        )

        self.sprite_list.append(self)
        self.timer: Timer = Timer(self.clock, duration)

    def update(self) -> None:
        if self.timer.available():
            self.kill()
