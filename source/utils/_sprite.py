from abc import ABC, abstractmethod
from typing import ClassVar

import arcade

from .classes import Clock, TuplePoint


class Sprite(arcade.Sprite, ABC):
    clock: ClassVar[Clock]

    def __init__(
        self,
        filename: str,
        rotation: float = 0,
        position: TuplePoint = (0, 0),
    ) -> None:
        super().__init__(
            filename,
            angle=rotation,
            center_x=position[0],
            center_y=position[1],
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
    def position(self) -> TuplePoint:
        return (self.x, self.y)

    @position.setter
    def position(self, __value: TuplePoint) -> None:  # type: ignore
        self.center_x = __value[0]
        self.center_y = __value[1]

    @abstractmethod
    def on_update(self, dt: float) -> None:  # type: ignore
        raise NotImplementedError
