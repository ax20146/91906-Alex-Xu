# /entities/particles/coins.py
"""`Coins` module containing the `Coin` particle sprite class."""


# Import Local Dependencies
from ...utils import Vector
from ...utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from ...utils.types import ClassVar
from . import particles


# Define Coin class
class Coin(particles.Particle):
    """`Coin` object represents a coin particle sprite.

    Inherited from `Particle`.

    Implements the functionality of a coin particle sprite.
    """

    # Define class attributes expected to be assigned
    # NOTE: Class attributes expected to be assigned:
    # sprite_list: ClassVar[arcade.SpriteList]
    target: ClassVar[Vector]

    # Define class constants
    LIFETIME = 8000
    COLLECTION_SPEED = 3
    COLLECTION_RANGE = TILE_SIZE

    # Define class constants expected to be override
    FILENAME: ClassVar[str]
    VALUE: ClassVar[int]

    def __init__(self, position: Vector) -> None:
        """Initialise a `Coin` particle sprite object.

        Args:
            position (Vector): The position of sprite.
        """

        # Initialised parent class
        super().__init__(
            self.FILENAME,
            position.randomise(TILE_SIZE).limit(
                Vector(), Vector(SCREEN_WIDTH, SCREEN_HEIGHT)
            ),
            duration=self.LIFETIME,
        )

    def on_collect(self) -> int:
        """Event called to collect the coin object.

        Returns:
            int: The value of the coin.
        """

        self.kill()
        return self.VALUE

    def update(self) -> None:
        """The update functionality for coin class."""
        super().update()

        # If able move towards the target position
        if self.xy.within(self.target, self.COLLECTION_RANGE):
            self.move(self.target, self.COLLECTION_SPEED)


# Define Gold coin
class Gold(Coin):
    """`Gold` coin particle sprite object.

    Inherited from `Coin`.
    """

    FILENAME = "./assets/Entities/Coins/Gold.png"
    VALUE = 5


# Define Silver coin
class Silver(Coin):
    """`Silver` coin particle sprite object.

    Inherited from `Coin`.
    """

    FILENAME = "./assets/Entities/Coins/Silver.png"
    VALUE = 1
