# /entities/entities/reinforcements.py
"""`Reinforcements` module containing the
`Reinforcement` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils.constants import TILE_SIZE
from ...utils.types import ClassVar
from . import enemies, entities, tanks


# Define Reinforcement class
class Reinforcement(entities.Entity):
    """`Reinforcement` object represents a reinforcement entity sprite.

    Inherited from `Entity`.

    Implements the functionality of a reinforcement entity sprite.
    """

    # Define class attributes expected to be assigned
    # NOTE: Class attributes expected to be assigned:
    # sprite_list: ClassVar[arcade.SpriteList]
    # waypoints: ClassVar[tuple[Vector, ...]]
    targets: ClassVar[arcade.SpriteList]

    # Define class constants expected to be override
    # NOTE: Class constants expected to be override
    # FILENAME: ClassVar[str]
    # HEALTH: ClassVar[int]
    # SPEED: ClassVar[float]
    PRICE: ClassVar[int]
    COOLDOWN: ClassVar[int]

    @classmethod
    def affordable(cls, amount: int) -> bool:
        """Determine whether the reinforcement entity is affordable.

        Args:
            amount (int): The given amount of coins.

        Returns:
            bool: Whether it is affordable.
        """

        return amount >= cls.PRICE

    def on_collide(self) -> None:
        """Event called when colliding with enemy entity."""

        # Find all enemies colliding with reinforcement entity
        sprites: list[arcade.Sprite] = arcade.check_for_collision_with_list(
            self, self.targets
        )

        # Check if there is colliding enemies
        if not sprites or not isinstance(sprites[0], enemies.Enemy):
            return

        # Select the colliding enemy as target
        target: enemies.Enemy = sprites[0]

        # Deal damage & take damage to & from target
        damage: int = max(target.health, 0)
        target.health -= max(self.health, 0)
        self.health -= damage

    def update(self) -> None:
        """The update functionality for reinforcement class."""
        super().update()

        # Determine if reinforcement entity should die
        if self.is_end() or self.is_dead():
            return self.on_die()

        # Check for collision with enemies
        self.on_collide()


# Define Truck reinforcement
class Truck(Reinforcement):
    """`Truck` reinforcement entity sprite object.

    Inherited from `Reinforcement`.
    """

    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 50
    SPEED = 2
    PRICE = 40
    COOLDOWN = 3500


# Define Tank reinforcement
class Tank(Reinforcement, tanks.Tank):
    """`Tank` reinforcement entity sprite object.

    Inherited from `Reinforcement` & `Tank`.
    """

    FILENAME = "./assets/Entities/Vehicles/TankSmall.png"
    HEALTH = 75
    SPEED = 1
    PRICE = 120
    COOLDOWN = 7500

    CANON_FILENAME = "./assets/Entities/Vehicles/TankSmallGun.png"
    FIRERATE = 1000
    DAMAGE = 12
    RANGE = int(3.5 * TILE_SIZE)


# Define list of all reinforcements mapped to button file
reinforcements: dict[type[Reinforcement], str] = {
    Truck: "./assets/UI/Truck.png",
    Tank: "./assets/UI/Tank.png",
}
