# /particle.py


from .utils import Sprite, VectorTuple


class Particle(Sprite):
    def __init__(
        self, filename: str, rotation: float, position: VectorTuple
    ) -> None:
        super().__init__(filename, rotation, position)

        self.life_time: int = 200
        self.created_time: float = self.clock.now()

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
