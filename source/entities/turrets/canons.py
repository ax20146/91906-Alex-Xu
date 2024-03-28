# /entities/turrets/canons.py


from ..particles.flames import SmallFlame
from .turrets import Turret


class TankCanon(Turret):
    def attack(self) -> None:
        super().attack()

        if not self.target:
            return

        SmallFlame(
            (self.xy - self.target.xy).normalise() * (self.height // 1.2),
            self.angle,
            min(self.timer.duration // 2, 200),
        )
