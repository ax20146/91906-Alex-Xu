# /entities/particles.py


from ..utils import Sprite, Timer, Vector
from ..utils.functions import cos, sin
from ..utils.types import ClassVar, final

__all__: list[str] = [
    "Flame",
    "BigFlame",
    "SmallFlame",
]


class Flame(Sprite):
    LENGTH = 54

    FILENAME: ClassVar[str]

    def __init__(
        self,
        rotation: float,
        position: Vector,
        lifetime: int,
    ) -> None:
        super().__init__(
            filename=self.FILENAME,
            rotation=rotation,
            position=position,
        )

        self.timer: Timer = Timer(self.clock, delay=lifetime)
        self.place()

    def place(self) -> None:
        self.x -= self.LENGTH * sin(self.radians)
        self.y += self.LENGTH * cos(self.radians)

    def on_update(self, delta_time: float) -> None:
        if self.timer.available():
            self.kill()


@final
class BigFlame(Flame):
    FILENAME = "/assets/Particles/FlameBig.png"


@final
class SmallFlame(Flame):
    FILENAME = "./assets/Particles/FlameSmall.png"
