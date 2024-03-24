# /entities/particles.py


from ..utils import Sprite, Timer, Vector
from ..utils.functions import cos, sin
from ..utils.types import TypeAlias, final

__all__: list[str] = [
    "Flame",
    "Flames",
    "BigFlame",
    "SmallFlame",
]


class Flame(Sprite):
    def __init__(
        self,
        filename: str,
        *,
        rotation: float,
        position: Vector,
        lifetime: int,
    ) -> None:
        super().__init__(
            filename,
            rotation=rotation,
            position=position,
        )

        self.sprite_list.append(self)

        self.timer: Timer = Timer(self.clock, delay=lifetime)
        self.place()

    def place(self) -> None:
        length: float = self.height // 1.2

        self.x -= length * sin(self.radians)
        self.y += length * cos(self.radians)

    def on_update(self, dt: float) -> None:
        if self.timer.available():
            self.kill()


@final
class BigFlame(Flame):
    def __init__(
        self,
        rotation: float,
        position: Vector,
        *,
        lifetime: int,
    ) -> None:
        super().__init__(
            "./assets/Particles/FlameBig.png",
            rotation=rotation,
            position=position,
            lifetime=lifetime,
        )


@final
class SmallFlame(Flame):
    def __init__(
        self,
        rotation: float,
        position: Vector,
        *,
        lifetime: int,
    ) -> None:
        super().__init__(
            "./assets/Particles/FlameSmall.png",
            rotation=rotation,
            position=position,
            lifetime=lifetime,
        )


Flames: TypeAlias = type[BigFlame | SmallFlame]
