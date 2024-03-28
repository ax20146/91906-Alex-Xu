# /utils/classes/sprite.py


import arcade

from ..types import ClassVar
from .clock import Clock
from .vector import Vector


class Sprite(arcade.Sprite):
    clock: ClassVar[Clock]

    def __init__(
        self,
        *,
        filename: str,
        position: Vector,
        rotation: float = 0,
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
    def xy(self) -> Vector:
        return Vector(*self.position)

    @xy.setter
    def xy(self, __value: Vector) -> None:
        self.position = __value.convert()

    def update(self) -> None:
        pass
