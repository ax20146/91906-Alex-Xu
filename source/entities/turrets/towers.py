# /entities/turrets/towers.py
"""`Towers` module containing the `Tower` sprite class."""


# Import Local Dependencies
from ...utils import Vector
from ...utils.constants import TILE_SIZE
from ...utils.types import ClassVar
from ..particles import flames, rockets
from . import turrets


# Define Tower class
class Tower(turrets.Turret):
    """`Tower` object represents a tower turret sprite.

    Inherited from `Turret`.

    Implements the functionality of a tower turret sprite.
    """

    # Define class attributes expected to be assigned
    # NOTE: Class attributes expected to be assigned:
    # sprite_list: ClassVar[arcade.SpriteList]
    # targets: ClassVar[arcade.SpriteList]

    # Define class constants expected to be override
    # NOTE: Class constants expected to be override
    # FILENAME: ClassVar[str]
    # FIRERATE: ClassVar[int]
    # DAMAGE: ClassVar[int]
    # RANGE: ClassVar[int]
    PRICE: ClassVar[int]

    def __init__(self, position: Vector) -> None:
        """Initialise a `Tower` sprite object.

        Args:
            position (Vector): The position of sprite.
        """

        # Initialised parent class
        super().__init__(position, add=True)

    @classmethod
    def affordable(cls, amount: int) -> bool:
        """Determine whether the tower turret is affordable.

        Args:
            amount (int): The given amount of coins.

        Returns:
            bool: Whether it is affordable.
        """

        return amount >= cls.PRICE

    def attack(self) -> None:
        """Function called when tower attacks."""
        super().attack()

        # Check if turret has a target
        if not self.target:
            return

        # Calculate the position of particle
        position: Vector = self.xy - (
            self.xy - self.target.xy
        ).normalise() * (self.height // self.LENGTH_RATIO)

        # Instantiate the particle when firing
        flames.BigFlame(
            position,
            self.angle,
            min(
                self.FIRERATE // self.PARTICLE_LIFETIME_RATIO,
                self.PARTICLE_LIFETIME,
            ),
        )


# Define Canon tower
class Canon(Tower):
    """`Canon` tower turret sprite object.

    Inherited from `Tower`.
    """

    FILENAME = "./assets/Entities/Towers/Canon.png"
    FIRERATE = 1000
    DAMAGE = 4
    RANGE = 4 * TILE_SIZE
    PRICE = 20


# Define MachineGun tower
class MachineGun(Tower):
    """`MachineGun` tower turret sprite object.

    Inherited from `Tower`.
    """

    FILENAME = "./assets/Entities/Towers/Gun.png"
    FIRERATE = 150
    DAMAGE = 1
    RANGE = 3 * TILE_SIZE
    PRICE = 45


# Define Rocket tower
class Rocket(Tower):
    """`RocketLauncher` tower turret sprite object.

    Inherited from `Tower`.
    """

    FILENAME = "./assets/Entities/Towers/Rocket.png"
    FIRERATE = 2000
    DAMAGE = 20
    RANGE = int(3.5 * TILE_SIZE)
    PRICE = 120

    PROJECTILE_RADIUS = int(TILE_SIZE // 1.2)
    PROJECTILE_SPEED = 8

    def attack(self) -> None:
        """Function called when rocket launcher attacks."""

        # Check if turret has a target
        if not self.target:
            return

        # Instantiate the rocket when firing
        rockets.Rocket(
            self.xy,
            self.target.xy,
            targets=self.targets,
            damage=self.DAMAGE,
            range=self.PROJECTILE_RADIUS,
            speed=self.PROJECTILE_SPEED,
        )


# Define list of all towers mapped to button file
towers: dict[type[Tower], str] = {
    Rocket: "./assets/UI/Rocket.png",
    MachineGun: "./assets/UI/Gun.png",
    Canon: "./assets/UI/Canon.png",
}
