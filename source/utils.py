# /utils.py


# Import Built-in Dependencies
from abc import ABC, abstractmethod
from typing import ClassVar

# Import 3rd-Party Dependencies
import arcade

# Define Constants
SCREEN_SIZE = (1280, 960)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]

# Layer
LAYER_MAP = "Map"
LAYER_SLOTS = "Slots"
LAYER_WAYPOINTS = "Waypoints"


# Define Types
VectorTuple = tuple[float, float]


class Clock:
    def __init__(self) -> None:
        self.time: float = 0

    def now(self) -> float:
        return self.time

    def update(self, dt: float) -> None:
        self.time += dt * 1000


class Sprite(arcade.Sprite, ABC):
    clock: ClassVar[Clock]

    def __init__(
        self,
        filename: str,
        rotation: float = 0,
        position: VectorTuple = (0, 0),
    ) -> None:
        super().__init__(
            filename,
            angle=rotation,
            center_x=position[0],
            center_y=position[1],
        )

    @abstractmethod
    def on_update(self, dt: float) -> None:  # type: ignore
        raise NotImplementedError


class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Vector):
            return NotImplemented

        return self.x == __value.x and self.y == __value.y

    def __gt__(self, __value: "Vector") -> bool:
        return self.x > __value.x and self.y > __value.y

    def __lt__(self, __value: "Vector") -> bool:
        return self.x < __value.x and self.y < __value.y

    def __add__(self, __value: "Vector | VectorTuple | float") -> "Vector":
        if isinstance(__value, tuple):
            return self.__class__(self.x + __value[0], self.y + __value[1])

        if isinstance(__value, (int, float)):
            return self.__class__(self.x + __value, self.y + __value)

        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: "Vector | VectorTuple | float") -> "Vector":
        if isinstance(__value, tuple):
            return self.__class__(self.x - __value[0], self.y - __value[1])

        if isinstance(__value, (int, float)):
            return self.__class__(self.x - __value, self.y - __value)

        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __repr__(self) -> str:
        return f"{self.__class__}({self.x}, {self.y})"

    def convert(self) -> VectorTuple:
        return (self.x, self.y)


__all__: list[str] = [
    "Clock",
    "Sprite",
    "Vector",
    "VectorTuple",
]
