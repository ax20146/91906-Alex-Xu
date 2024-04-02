# /entities/particles/flames.py
"""`Flames` module containing the `Flame` particle sprite class."""


# Import Local Dependencies
from ...utils import Vector
from ...utils.types import ClassVar
from . import particles


# Define Flame class
class Flame(particles.Particle):
    """`Flame` object represents a flame particle sprite.

    Inherited from `Particle`.

    Implements the functionality of a flame particle sprite.
    """

    # Define class constants expected to be override
    FILENAME: ClassVar[str]

    def __init__(
        self, position: Vector, rotation: float, duration: int
    ) -> None:
        """Initialise a `Flame` particle sprite object.

        Args:
            position (Vector): The position of sprite.
            rotation (float): The rotation of sprite.
            duration (int): The particle lifetime duration.
        """

        # Initialised parent class
        super().__init__(
            self.FILENAME,
            position,
            rotation,
            duration=duration,
        )


# Define BigFlame flame
class BigFlame(Flame):
    """`BigFlame` flame particle sprite object.

    Inherited from `Flame`.
    """

    FILENAME = "./assets/Particles/FlameBig.png"


# Define SmallFlame flame
class SmallFlame(Flame):
    """`SmallFlame` flame particle sprite object.

    Inherited from `Flame`.
    """

    FILENAME = "./assets/Particles/FlameSmall.png"
