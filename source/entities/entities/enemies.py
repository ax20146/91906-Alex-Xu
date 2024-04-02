# /entities/entities/enemies.py
"""`Enemies` module containing the `Enemy` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils.constants import TILE_SIZE
from ...utils.types import ClassVar
from ..particles import coins
from . import entities, tanks


# Define Enemy class
class Enemy(entities.Entity):
    """`Enemy` object represents a enemy entity sprite.

    Inherited from `Entity`.

    Implements the functionality of a enemy entity sprite.
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
    DROPS: ClassVar[tuple[type[coins.Coin], int]]

    def on_end(self) -> int:
        """Event called when enemy reached end.

        Returns:
            int: The remaining health of enemy.
        """

        self.on_die()
        return self.health

    def on_die(self) -> None:
        """Event called when enemy dies."""

        super().on_die()

        # Drop the defined coin type & number of coins
        coin, amount = self.DROPS
        for _ in range(amount):
            coin(self.xy)


# Define Soldier enemy
class Soldier(Enemy):
    """`Soldier` enemy entity sprite object.

    Inherited from `Enemy`.
    """

    FILENAME = "./assets/Entities/Troops/Soldier.png"
    HEALTH = 10
    SPEED = 2
    DROPS = (coins.Bronze, 2)


# Define Zombie enemy
class Zombie(Enemy):
    """`Zombie` enemy entity sprite object.

    Inherited from `Enemy`.
    """

    FILENAME = "./assets/Entities/Troops/Zombie.png"
    HEALTH = 8
    SPEED = 3
    DROPS = (coins.Bronze, 3)


# Define Knight enemy
class Knight(Enemy):
    """`Knight` enemy entity sprite object.

    Inherited from `Enemy`.
    """

    FILENAME = "./assets/Entities/Troops/Knight.png"
    HEALTH = 35
    SPEED = 1
    DROPS = (coins.Gold, 1)


# Define Robot enemy
class Robot(Enemy):
    """`Robot` enemy entity sprite object.

    Inherited from `Enemy`.
    """

    FILENAME = "./assets/Entities/Troops/Robot.png"
    HEALTH = 30
    SPEED = 2
    DROPS = (coins.Gold, 2)


# Define Tank enemy
class Tank(Enemy, tanks.Tank):
    """`Tank` enemy entity sprite object.

    Inherited from `Enemy` & `Tank`.
    """

    FILENAME = "./assets/Entities/Vehicles/TankBig.png"
    HEALTH = 250
    SPEED = 1
    DROPS = (coins.Gold, 5)

    CANON_FILENAME = "./assets/Entities/Vehicles/TankBigGun.png"
    FIRERATE = 2500
    DAMAGE = 35
    RANGE = 4 * TILE_SIZE
