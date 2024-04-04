# /entities/particles/particles.py
"""`Particles` module containing the `Particle` sprite class."""


# Import Local Dependencies
from ...utils import Sprite, Timer, Vector


# Define Particle class
class Particle(Sprite):
    """`Particle` object represents a particle sprite.

    Inherited from `Sprite`.

    Implements the base functionality of a particle sprite.
    """

    # NOTE: Class attributes expected to be assigned:
    # sprite_list: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        filename: str,
        position: Vector,
        rotation: float = 0,
        *,
        duration: int = 0,
    ) -> None:
        """Initialise a `Particle` sprite object.

        Args:
            filename (str): The file of sprite.
            position (Vector): The position of sprite.
            rotation (float, optional): The rotation of sprite.
                Defaults to 0.
            duration (int, optional): The particle lifetime duration.
                Defaults to 0.
        """

        # Initialised parent class
        super().__init__(
            filename,
            position,
            rotation,
            add=True,
        )

        # Define attributes of particle
        self.timer: Timer = Timer(self.clock, duration)

    def update(self) -> None:
        """The update functionality for particle class."""

        # Kill particle when its lifetime is over
        if self.timer.available():
            self.kill()
