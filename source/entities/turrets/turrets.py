# /entities/turrets/turrets.py
"""`Turrets` module containing the `Turret` sprite class."""


# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from ...utils import Sprite, Timer, Vector
from ...utils.types import ClassVar
from ..entities import entities


# Define Turret class
class Turret(Sprite):
    """`Turret` object represents a turret sprite.

    Inherited from `Sprite`.

    Implements the base functionality of a Turret sprite.
    """

    # Define class attributes expected to be override
    targets: ClassVar[arcade.SpriteList]

    # Define class constants
    RELOAD_RATIO = 3
    LENGTH_RATIO = 1.2
    PARTICLE_LIFETIME = 150
    PARTICLE_LIFETIME_RATIO = 2

    # Define class constants expected to be override
    FILENAME: ClassVar[str]
    FIRERATE: ClassVar[int]
    DAMAGE: ClassVar[int]
    RANGE: ClassVar[int]

    def __init__(self, position: Vector, *, add: bool = False) -> None:
        """Initialise a `Turret` sprite object.

        Args:
            position (Vector): The position of sprite.
            add (bool, optional):
            The option to add to sprite list during initialisation.
                Defaults to False.
        """

        # Initialised parent class
        super().__init__(self.FILENAME, position, add=add)

        # Define attributes of turret
        self.target: entities.Entity | None
        self.timer: Timer = Timer(self.clock, self.FIRERATE)
        self.reload: Timer = Timer(
            self.clock, self.FIRERATE // self.RELOAD_RATIO
        )

    def attack(self) -> None:
        """Function called when turret attacks."""

        # Check if turret has a target
        if not self.target:
            return

        # Deduct health from enemy
        self.target.health -= self.DAMAGE

    def update_target(self) -> None:
        """Update the turret target entity."""

        self.target = None

        # Determine the target entity who is travelled the furthest
        for target in (
            sprite
            for sprite in self.targets
            if isinstance(sprite, entities.Entity)
            and self.xy.within(sprite.xy, self.RANGE)
        ):
            self.target = self.target or target

            # The condition to determine whether the entity travelled
            # more distance than current selected target
            condition: bool = target.target_idx > self.target.target_idx or (
                target.target_idx == self.target.target_idx
                and target.distance() < self.target.distance()
            )

            # Assign new targets if current target travelled less
            self.target = target if condition else self.target

    def update(self) -> None:
        """The update functionality for turret class."""

        # Determine if turret finished reloading and has a target
        self.update_target()
        if not self.reload.available() or not self.target:
            return

        # Rotate towards the selected target
        self.rotate(self.target.xy)

        # Determine if turret is able to attack
        if self.timer.available():
            self.attack()
            self.reload.update()
            self.timer.update()
