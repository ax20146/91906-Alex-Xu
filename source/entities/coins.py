# /entities/coins.py


from ..utils import Sprite, Timer, Vector
from ..utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from ..utils.types import final


class Coin(Sprite):
    LIFETIME = 8000

    FILENAME: str
    VALUE: int

    def __init__(self, position: Vector) -> None:
        super().__init__(
            filename=self.FILENAME,
            position=position.randomise(TILE_SIZE).limit(
                Vector(), Vector(SCREEN_WIDTH, SCREEN_HEIGHT)
            ),
        )

        self.timer: Timer = Timer(self.clock, self.LIFETIME)

    def on_collect(self) -> int:
        self.kill()
        return self.VALUE

    def update(self) -> None:
        if self.timer.available():
            self.kill()


@final
class Gold(Coin):
    FILENAME = "./assets/Entities/Coins/Gold.png"
    VALUE = 15


@final
class Silver(Coin):
    FILENAME = "./assets/Entities/Coins/Silver.png"
    VALUE = 5


@final
class Bronze(Coin):
    FILENAME = "./assets/Entities/Coins/Bronze.png"
    VALUE = 1
