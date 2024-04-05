# /entities/entities/tanks.py
"""`Tanks` module containing the `Tanks` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils import Vector
from ...utils.constants import TRANSPARENT_LIGHT
from ...utils.types import ClassVar
from ..particles import flames
from ..turrets import turrets
from . import entities


# Define Canon class
class Canon(turrets.Turret):
    """`Canon` object represents a canon turret sprite.

    Inherited from `Turret`.

    Implements the functionality of a canon turret sprite.
    """

    def __init__(
        self,
        filename: str,
        position: Vector,
        *,
        firerate: int,
        damage: int,
        range: int,
        targets: arcade.SpriteList,
    ) -> None:
        """Initialise a `Canon` turret sprite object.

        Args:
            filename (str): The file of canon.
            position (Vector): The position of canon.
            firerate (int): The firerate of canon.
            damage (int): The damage of canon.
            range (int): The range of canon
            targets (arcade.SpriteList): The list of potential targets.
        """

        # Define attributes of canon
        self.targets = targets
        self.FILENAME = filename
        self.FIRERATE = firerate
        self.DAMAGE = damage
        self.RANGE = range

        # Initialised parent class
        super().__init__(position)

    def attack(self) -> None:
        """Function called when canon attacks."""
        super().attack()

        # Check if turret has a target
        if not self.target:
            return

        # Calculate the position of particle
        position: Vector = self.xy - (
            self.xy - self.target.xy
        ).normalise() * (self.height // self.LENGTH_RATIO)

        # Instantiate the particle when firing
        flames.SmallFlame(
            position,
            self.angle,
            min(
                self.FIRERATE // self.PARTICLE_LIFETIME_RATIO,
                self.PARTICLE_LIFETIME,
            ),
        )


# Define Tank class
class Tank(entities.Entity):
    """`Tank` object represents a tank entity sprite.

    Inherited from `Entity`.

    Implements the functionality of a tank entity sprite.
    """

    # Define class attributes expected to be override
    # NOTE: Class attributes expected to be override:
    # sprite_list: ClassVar[arcade.SpriteList]
    # waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]

    # Define class constants expected to be override
    # NOTE: Class constants expected to be override
    # FILENAME: ClassVar[str]
    # HEALTH: ClassVar[int]
    # SPEED: ClassVar[float]
    CANON_FILENAME: ClassVar[str]
    FIRERATE: ClassVar[int]
    DAMAGE: ClassVar[int]
    RANGE: ClassVar[int]

    def __init__(self) -> None:
        """Initialise a `Tank` entity sprite object."""

        # Initialised parent class
        super().__init__()

        # Instantiate the tank canon object
        self.canon: Canon = Canon(
            self.CANON_FILENAME,
            self.xy,
            firerate=self.FIRERATE,
            damage=self.DAMAGE,
            range=self.RANGE,
            targets=self.targets,
        )

        # Initial setup for tank canon
        self.sprite_list.append(self.canon)
        self.canon.rotate(self.waypoints[self.target_idx])

    def update(self) -> None:
        """The update functionality for tank class."""
        super().update()

        # Move & update the tank canon
        self.canon.xy = self.xy
        self.canon.update()

        # Rotate the tank canon when it has no target
        if (
            not self.canon.target
            and self.canon.reload.available()
            and not self.is_end()
        ):
            self.canon.rotate(self.waypoints[self.target_idx])

    def on_select_draw(self) -> None:
        """Event called when tank is selected."""

        # Draw the range of tank canon
        arcade.draw_circle_filled(
            self.x,
            self.y,
            radius=self.RANGE,
            color=TRANSPARENT_LIGHT,
        )

        super().on_select_draw()

    def on_die(self) -> None:
        """Event called when tank dies."""
        super().on_die()

        # Kill the tank canon
        self.canon.kill()
