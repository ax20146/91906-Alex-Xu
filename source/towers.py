from typing import final

from .entities import TurretEntity
from .flames import BigFlame
from .utils import ClassSpriteList, TuplePoint
from .utils.constants import Cooldown, Damage, Duration, Price, Range


class Tower(TurretEntity):
    lst: ClassSpriteList

    def __init__(
        self,
        filename: str,
        *,
        position: tuple[float, float],
        damage: int,
        range: int,
        cooldown: int,
        price: int,
    ) -> None:
        super().__init__(
            filename,
            position,
            damage=damage,
            range=range,
            cooldown=cooldown,
        )

        self.lst.append(self)
        self.price: int = price

    def attack(self) -> None:
        self.target.health -= self.damage


@final
class Canon(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Canon.png",
            position=position,
            damage=Damage.HIGH,
            range=Range.FAR,
            cooldown=Duration.LONG,
            price=Price.MEDIUM,
        )

    def attack(self) -> None:
        super().attack()
        BigFlame(self.angle, self.position, delay=Duration.SHORTER)


@final
class MachineGun(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Gun.png",
            position=position,
            damage=Damage.LOW,
            range=Range.SHORT,
            cooldown=Duration.SHORTER,
            price=Price.LOW,
        )

    def attack(self) -> None:
        super().attack()
        BigFlame(self.angle, self.position, delay=Duration.SHORTEST)


@final
class RocketLauncher(Tower):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Towers/Rocket.png",
            position=position,
            damage=Damage.MEDIUM,
            range=Range.SHORT,
            cooldown=Cooldown.MEDIUM,
            price=Price.MEDIUM,
        )

    def attack(self) -> None:
        super().attack()
        ...


Towers = type[Canon | MachineGun | RocketLauncher]
