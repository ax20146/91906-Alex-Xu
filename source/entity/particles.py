# Import Dependencies
from math import cos, sin

from ..utils import Sprite, VectorTuple


# Define Particle Class
class Particle(Sprite):
    def __init__(
        self,
        filename: str,
        rotation: float,
        position: VectorTuple,
    ) -> None:
        super().__init__(
            filename,
            rotation=rotation,
            position=position,
        )

        self.born_time: float = self.clock.now()
        self.place()

    def place(self) -> None:
        length: float = self.height // 1.5
        angle: float = self.radians

        self.center_x -= length * sin(angle)
        self.center_y += length * cos(angle)

    def on_update(self, dt: float) -> None:
        if self.clock.now() - self.born_time >= 100:
            self.kill()
