# /utils/classes/sprite.py
"""`Sprite` module containing the custom `Sprite` class."""


# Import Built-in Dependencies
from typing import ClassVar

# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from .clock import Clock
from .vector import Vector


# Define Sprite class
class Sprite(arcade.Sprite):
    """`Sprite` object represents a sprite.

    Inherited from `arcade.Sprite`.

    Implements & overrides some functionality of the `arcade.Sprite`.
    """

    # Define class attributes
    clock: ClassVar[Clock]

    # Define class attributes expected to be override
    sprite_list: ClassVar[arcade.SpriteList]

    def __init__(
        self,
        filename: str,
        position: Vector,
        rotation: float = 0,
        *,
        add: bool = False,
    ) -> None:
        """Initialise a `Sprite` object.

        Args:
            filename (str): The file of sprite.
            position (Vector): The position of sprite.
            rotation (float, optional): The rotation of sprite.
                Defaults to 0.
            add (bool, optional):
            The option to add to sprite list during initialisation.
                Defaults to False.
        """

        # Initialised `arcade.Sprite`
        super().__init__(
            filename,
            center_x=position.x,
            center_y=position.y,
            angle=rotation,
        )

        # Adding to sprite list based on 'add' parameter
        if add is True:
            self.sprite_list.append(self)

    @property
    def x(self) -> float:
        """The x position of sprite.

        Returns:
            float: The x position.
        """

        return self.center_x

    @property
    def y(self) -> float:
        """The y position of sprite.

        Returns:
            float: The y position.
        """

        return self.center_y

    @property
    def xy(self) -> Vector:
        """The xy position of sprite using vector.

        Returns:
            Vector: The xy vector of sprite position.
        """

        return Vector(*self.position)

    @xy.setter
    def xy(self, __value: Vector) -> None:
        """Set the xy position of sprite using vector.

        Args:
            __value (Vector): The vector to set sprite position.
        """

        self.position = __value.convert()

    def name(self) -> str:
        """The name of the sprite class in a readable format.

        Returns:
            str: The sprite class name.
        """

        # Retrieve class name
        name: str = self.__class__.__name__

        # Retrieve the 1st character of sprite class name
        # Iterates other characters, add space when encounter uppercase
        return name[0] + str().join(
            f" {char}" if char.isupper() else char for char in name[1:]
        )

    def move(self, direction: Vector, speed: float) -> None:
        """Move the sprite towards given 'direction' with given 'speed'.

        Args:
            direction (Vector): The target position vector to move to.
            speed (float): The speed to travel at.
        """

        # Calculate the movement vector
        movement: Vector = direction - self.xy

        # Move sprite precise steps to reach its target when close by
        if movement.length() < speed:
            self.xy += movement
            return

        # Otherwise move towards 'direction' by the given 'speed'
        # Rounded to the nearest pixel to avoid texture pixilation
        self.xy += round(movement.normalise() * speed)

    def rotate(self, direction: Vector) -> None:
        """Rotate the sprite towards given 'direction' (point).

        Args:
            direction (Vector): The target position vector to rotate to.
        """

        self.face_point(direction.convert())

    def update(self) -> None:
        """OVERRIDE: The update function called every cycle (tick)."""
        pass
