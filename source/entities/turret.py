import arcade

from ..utils import Sprite, Timer, Vector
from ..utils.constants import TILE_SIZE
from ..utils.types import ClassVar
from .entity import Entity


class Turret(Sprite):
    targets: ClassVar[arcade.SpriteList]

    FILENAME: str
    COOLDOWN: int
    DAMAGE: int
    RANGE: int

    def __init__(self, position: Vector) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=position,
        )

        self.timer: Timer = Timer(self.clock, self.COOLDOWN)
        self.reload: Timer = Timer(self.clock, self.COOLDOWN // 3)

        self.target: Entity | None = None

    def update_target(self) -> None:
        if not (
            sprites := [
                sprite
                for sprite in self.targets
                if isinstance(sprite, Entity)
                and self.xy.within(sprite.xy, self.RANGE * TILE_SIZE)
            ]
        ):
            self.target = None
            return

        self.target = sprites[0]

    def update(self) -> None:
        self.update_target()

        if not self.reload.available() or self.target is None:
            return
        self.face_point(self.target.xy.convert())

        if self.timer.available():
            self.timer.update()
            self.reload.update()
            self.attack()

    def attack(self) -> None:
        if self.target is None:
            return

        self.target.health -= self.DAMAGE
