from .entity import TurretEntity
from .particles import Fire
from .utils import VectorTuple


class Tower(TurretEntity):
    def __init__(
        self,
        filename: str,
        position: VectorTuple,
        *,
        damage: int,
        range: int,
        cooldown: int,
        price: int,
    ) -> None:
        super().__init__(filename, position, damage, range, cooldown)

        self.price: int = price


class Canon(Tower):
    def __init__(self, position: VectorTuple) -> None:
        super().__init__(
            "./assets/Entity/Towers/Canon.png",
            position,
            damage=100,
            range=3 * 64,
            cooldown=1500,
            price=80,
        )

    def attack(self) -> None:
        self.target.health -= self.damage

        self.particles.append(Fire(self.angle, (self.x, self.y)))
