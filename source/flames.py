from math import cos, sin
from typing import final

from .entities import Particle
from .utils import TuplePoint


class Flame(Particle):
    def __init__(
        self,
        filename: str,
        *,
        rotation: float,
        position: TuplePoint,
        delay: int,
    ) -> None:
        super().__init__(
            filename,
            rotation=rotation,
            position=position,
            delay=delay,
        )

        length: float = self.height // 1.5
        angle: float = self.radians

        self.center_x -= length * sin(angle)
        self.center_y += length * cos(angle)


@final
class BigFlame(Flame):
    def __init__(
        self,
        rotation: float,
        position: TuplePoint,
        *,
        delay: int,
    ) -> None:
        super().__init__(
            "./assets/Particles/FlameBig.png",
            rotation=rotation,
            position=position,
            delay=delay,
        )


@final
class SmallFlame(Flame):
    def __init__(
        self,
        rotation: float,
        position: TuplePoint,
        *,
        delay: int,
    ) -> None:
        super().__init__(
            "./assets/Particles/FlameSmall.png",
            rotation=rotation,
            position=position,
            delay=delay,
        )


Particles = type[BigFlame | SmallFlame]
