# /entities/particles/rockets.py
"""`Rockets` module containing the `Rocket` particle sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils import Vector
from ...utils.types import Iterator
from ..entities import entities
from . import particles


# Define Rocket class
class Rocket(particles.Particle):
    """`Rocket` object represents a rocket particle sprite.

    Inherited from `Particle`.

    Implements the functionality of a rocket particle sprite.
    """

    # Define class constants
    FILENAME = "./assets/Particles/Rocket.png"

    def __init__(
        self,
        position: Vector,
        target: Vector,
        *,
        targets: arcade.SpriteList,
        damage: int,
        range: int,
        speed: float,
    ) -> None:
        """Initialise a `Rocket` particle sprite object.

        Args:
            position (Vector): The position of rocket.
            target (Vector): The position of target.
            targets (arcade.SpriteList): The list of potential targets.
            damage (int): The damage of rocket.
            range (int): The splash range of rocket.
            speed (float): The speed of rocket.
        """

        # Initialised parent class
        super().__init__(self.FILENAME, position)

        # Define attributes of canon
        self.target: Vector = target
        self.targets: arcade.SpriteList = targets
        self.SPEED: float = speed
        self.RANGE: int = range
        self.DAMAGE: int = damage

        # Rotate the rocket towards target
        self.rotate(self.target)

    def explode(self) -> None:
        """Function called when rocket explodes."""

        # Determine the target entity within splash range
        sprites: Iterator[entities.Entity] = (
            sprite
            for sprite in self.targets
            if isinstance(sprite, entities.Entity)
            and arcade.get_distance_between_sprites(self, sprite)
            <= self.RANGE
        )

        # Deduct health from enemies within splash range
        for target in sprites:
            target.health -= self.DAMAGE

    def update(self) -> None:
        """The update functionality for rocket class."""

        # Move & rotate towards the select target position
        self.move(self.target, self.SPEED)

        # Determine if rocket reached target position
        if self.xy == self.target:
            self.explode()
            self.kill()
