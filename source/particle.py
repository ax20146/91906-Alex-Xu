# /particle.py


from math import cos, sin

from .utils import Sprite, VectorTuple


class Particle(Sprite):
    def __init__(
        self,
        filename: str,
        rotation: float,
        position: VectorTuple,
    ) -> None:
        super().__init__(
            filename=filename,
            rotation=rotation,
            position=position,
        )

        self.life_time: int = 100
        self.created_time: float = self.clock.now()
        self.place()

    def place(self):
        length: float = self.height // 1.5
        angle: float = self.radians

        self.center_x -= length * sin(angle)
        self.center_y += length * cos(angle)

    def on_update(self, dt: float) -> None:
        if self.clock.now() - self.created_time >= self.life_time:
            self.kill()


class Fire(Particle):
    def __init__(self, rotation: float, position: VectorTuple) -> None:
        super().__init__(
            "./assets/particles/turret_fire.png",
            rotation,
            position,
        )
