import arcade

from ..utils import Movement, Sprite, Vector
from ..utils.types import ClassVar
from .enemies import Enemy


class Rocket(Sprite):
    targets: ClassVar[arcade.SpriteList]

    FILENAME = "./assets/Particles/Rocket.png"
    RANGE = 50
    SPEED = 10

    def __init__(
        self, rotation: float, position: Vector, target: Vector, damage: int
    ) -> None:
        super().__init__(
            filename=self.FILENAME,
            rotation=rotation,
            position=position,
        )

        self.movement: Movement = Movement(self, self.SPEED, target)
        self.damage: int = damage

    def explode(self) -> None:
        sprites = (
            sprite
            for sprite in self.targets
            if isinstance(sprite, Enemy)
            and arcade.get_distance_between_sprites(self, sprite)
            <= self.RANGE
        )

        for target in sprites:
            target.health -= self.damage

    def update(self) -> None:
        self.movement.move()
        self.movement.rotate()

        if self.xy == self.movement.target:
            self.explode()
            self.kill()
