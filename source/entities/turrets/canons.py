# /entities/turrets/canons.py


from source.utils.classes.vector import Vector

from ..particles.flames import SmallFlame
from .turrets import Turret


class TankCanon(Turret):
    def attack(self) -> None:
        if not self.target:
            return

        super().attack()
        position: Vector = self.xy - (
            self.xy - self.target.xy
        ).normalise() * (self.height // 1.2)

        SmallFlame(
            position,
            self.angle,
            200,
        )
