from .coins import Gold
from .enemies import Enemy
from .entities import TurretEntity


class TankCanon(TurretEntity):
    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__(
            "./assets/Entity/Tanks/TankBigGun.png",
            position,
            damage=0,
            range=2,
            cooldown=1000,
        )

    def attack(self) -> None:
        print("Tank!")


class Tank(Enemy):
    def __init__(self) -> None:
        super().__init__(
            "./assets/Entity/Tanks/TankBig.png",
            speed=25,
            health=800,
            coin=(Gold, 10),
        )

        self.turret = TankCanon(self.position)

    def on_update(self, dt: float) -> None:
        self.turret.position = self.position
        self.turret.angle += 5
        super().on_update(dt)
