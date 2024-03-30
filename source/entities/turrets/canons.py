# /entities/turrets/canons.py


from ...utils import Vector
from ...utils.types import final
from .. import particles
from .turrets import Turret


@final
class TankCanon(Turret):
    def attack(self) -> None:
        if not self.target:
            return

        super().attack()
        position: Vector = self.xy - (
            self.xy - self.target.xy
        ).normalise() * (self.height // 1.2)

        particles.flames.SmallFlame(
            position,
            self.angle,
            100,
        )
