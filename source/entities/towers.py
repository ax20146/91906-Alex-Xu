from ..utils.types import final
from .flames import BigFlame
from .rockets import Rocket
from .turret import Turret


class Tower(Turret):
    PRICE: int
    PARTICLE_TIME: int

    def affordable(self, amount: int) -> bool:
        return amount >= self.PRICE

    def attack(self) -> None:
        super().attack()
        BigFlame(self.angle, self.xy, lifetime=self.PARTICLE_TIME)


@final
class Canon(Tower):
    FILENAME = "/assets/Entities/Towers/Canon.png"
    PRICE = 10
    DAMAGE = 10
    RANGE = 3
    COOLDOWN = 1000
    PARTICLE_TIME = 200


@final
class Gun(Tower):
    FILENAME = "./assets/Entities/Towers/Gun.png"
    PRICE = 10
    DAMAGE = 10
    RANGE = 3
    COOLDOWN = 1000
    PARTICLE_TIME = 50


@final
class RocketLauncher(Tower):
    FILENAME = "./assets/Entities/Towers/Rocket.png"
    PRICE = 10
    DAMAGE = 10
    RANGE = 3
    COOLDOWN = 1000

    def attack(self) -> None:
        if self.target is None:
            return

        Rocket(self.angle, self.xy, target=self.target.xy, damage=self.DAMAGE)
