from random import randint
from typing import final

from .entities import Particle
from .utils import TuplePoint
from .utils.constants import TILE_SIZE, Duration, Value


def randrange(value: float, range: int) -> int:
    return randint(round(value) - range, round(value) + range)


class Coin(Particle):
    def __init__(
        self,
        filename: str,
        *,
        position: TuplePoint,
        value: int,
    ) -> None:
        super().__init__(
            filename,
            position=(
                randrange(position[0], TILE_SIZE),
                randrange(position[1], TILE_SIZE),
            ),
            delay=Duration.LONGER,
        )

        self.value: int = value

    def on_collect(self, amount: int) -> int:
        self.kill()
        return amount + self.value


@final
class Gold(Coin):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Coins/Gold.png",
            position=position,
            value=Value.HIGH,
        )


@final
class Bronze(Coin):
    def __init__(self, position: TuplePoint) -> None:
        super().__init__(
            "./assets/Entity/Coins/Bronze.png",
            position=position,
            value=Value.LOW,
        )


Coins = type[Bronze | Gold]
