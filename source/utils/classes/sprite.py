# /utils/classes/sprite.py


# Import Built-In Dependencies
from abc import ABC, abstractmethod
from typing import ClassVar

# Import 3rd-Party Dependencies
import arcade

# Import Local Dependencies
from .clock import Clock
from .vector import Vector


# Define Sprite Class
class Sprite(arcade.Sprite, ABC):
    clock: ClassVar[Clock]

    def __init__(
        self,
        filename: str,
        *,
        rotation: float = 0,
        position: Vector = Vector(0, 0),
    ) -> None:
        super().__init__(
            filename,
            angle=rotation,
            center_x=position.x,
            center_y=position.y,
        )

    @property
    def x(self) -> float:
        return self.center_x

    @x.setter
    def x(self, __value: float) -> None:
        self.center_x = __value

    @property
    def y(self) -> float:
        return self.center_y

    @y.setter
    def y(self, __value: float) -> None:
        self.center_y = __value

    @property
    def position(self) -> Vector:  # type: ignore
        return Vector(self.x, self.y)

    @abstractmethod
    def on_update(self, dt: float) -> None:  # type: ignore
        pass
