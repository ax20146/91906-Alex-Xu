from random import randint
from typing import ClassVar

from .utils import Sprite, VectorTuple


class Coin(Sprite):
    amount: ClassVar[int]

    def __init__(
        self,
        filename: str,
        position: VectorTuple,
        *,
        value: int,
    ) -> None:
        super().__init__(
            filename,
            rotation=randint(1, 360),
            position=position,
        )

        self.value: int = value
        self.duration: int = 5000
        self.created: float = self.clock.now()

    def on_collect(self) -> None:
        self.kill()
        Coin.amount += self.value

    def on_update(self, dt: float) -> None:
        if self.clock.now() - self.created >= self.duration:
            self.kill()


class Gold(Coin):
    def __init__(self, position: VectorTuple) -> None:
        super().__init__(
            "./assets/Entity/Coins/Gold.png",
            position,
            value=50,
        )


class Bronze(Coin):
    def __init__(self, position: VectorTuple) -> None:
        super().__init__(
            "./assets/Entity/Coins/Bronze.png",
            position,
            value=20,
        )
