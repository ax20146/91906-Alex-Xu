# /entities/coins.py


from ..utils import Movement, Sprite, Timer, Vector
from ..utils.constants import TILE_SIZE
from ..utils.functions import limit_within, randrange
from ..utils.types import ClassVar, final

__all__: list[str] = [
    "Coin",
    "Gold",
    "Silver",
    "Bronze",
]


class Coin(Sprite):
    COLLECTION_RANGE = TILE_SIZE * 3
    LIFETIME = 8000
    SPEED = 25

    FILENAME: ClassVar[str]
    VALUE: ClassVar[int]

    def __init__(
        self,
        position: Vector,
    ) -> None:
        position = Vector(
            randrange(position.x, TILE_SIZE),
            randrange(position.y, TILE_SIZE),
        )

        super().__init__(
            filename=self.FILENAME,
            position=limit_within(position),
        )

        self.timer: Timer = Timer(self.clock, delay=self.LIFETIME)
        self.movement: Movement = Movement(self, self.SPEED)

    def attract(self, target: Vector) -> None:
        if self.position.within(target, radius=self.COLLECTION_RANGE):
            self.movement.update_target(target)

    def collect(self) -> int:
        self.kill()
        return self.VALUE

    def on_update(self, delta_time: float) -> None:
        if self.movement.has_target():
            self.movement.move(delta_time)

        if self.timer.available():
            self.kill()


@final
class Gold(Coin):
    FILENAME = "./assets/Entities/Coins/Gold.png"
    VALUE = 10


@final
class Silver(Coin):
    FILENAME = "./assets/Entities/Coins/Silver.png"
    VALUE = 5


@final
class Bronze(Coin):
    FILENAME = "./assets/Entities/Coins/Bronze.png"
    VALUE = 1
