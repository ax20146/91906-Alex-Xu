# /entities/particles/flames.py


from ...utils import Vector
from ...utils.types import ClassVar, final
from .particles import Particle


class Flame(Particle):
    FILENAME: ClassVar[str]

    def __init__(
        self, position: Vector, rotation: float = 0, duration: int = 0
    ) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=position,
            rotation=rotation,
            duration=duration,
        )


@final
class BigFlame(Flame):
    FILENAME = "./assets/Particles/FlameBig.png"


@final
class SmallFlame(Flame):
    FILENAME = "./assets/Particles/FlameSmall.png"
