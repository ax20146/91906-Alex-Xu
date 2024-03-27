from ..utils import Sprite, Timer, Vector
from ..utils.constants import TILE_SIZE
from ..utils.functions import cos, sin
from ..utils.types import final


class Flame(Sprite):
    LENGTH = TILE_SIZE // 54

    FILENAME: str

    def __init__(
        self, rotation: float, position: Vector, *, lifetime: int
    ) -> None:
        super().__init__(
            filename=self.FILENAME,
            rotation=rotation,
            position=position,
        )

        self.timer: Timer = Timer(self.clock, lifetime)
        self.place()

    def place(self) -> None:
        self.x -= self.LENGTH * sin(self.radians)
        self.y += self.LENGTH * cos(self.radians)

    def update(self) -> None:
        if self.timer.available():
            self.kill()


@final
class BigFlame(Flame):
    FILENAME = "./assets/Particles/FlameBig.png"


@final
class SmallFlame(Flame):
    FILENAME = "./assets/Particles/FlameSmall.png"
