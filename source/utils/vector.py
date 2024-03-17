# /vector.py

# Import Local Dependencies
from __future__ import annotations

# Define custom types
VectorTuple = tuple[float, float]


# Define vector class
class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Vector):
            return NotImplemented

        return self.x == __value.x and self.y == __value.y

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __gt__(self, __value: Vector | VectorTuple) -> bool:
        if isinstance(__value, tuple):
            return self.x > __value[0] and self.y > __value[1]

        return self.x > __value.x and self.y > __value.y

    def __ge__(self, __value: Vector | VectorTuple) -> bool:
        if isinstance(__value, tuple):
            return self.x >= __value[0] and self.y >= __value[1]

        return self.x >= __value.x and self.y >= __value.y

    def __lt__(self, __value: Vector | VectorTuple) -> bool:
        if isinstance(__value, tuple):
            return self.x < __value[0] and self.y < __value[1]

        return self.x < __value.x and self.y < __value.y

    def __le__(self, __value: Vector | VectorTuple) -> bool:
        if isinstance(__value, tuple):
            return self.x <= __value[0] and self.y <= __value[1]

        return self.x <= __value.x and self.y <= __value.y

    def __add__(self, __value: Vector | VectorTuple | float) -> Vector:
        if isinstance(__value, tuple):
            return self.__class__(self.x + __value[0], self.y + __value[1])

        if isinstance(__value, (int, float)):
            return self.__class__(self.x + __value, self.y + __value)

        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: Vector | VectorTuple | float) -> Vector:
        if isinstance(__value, tuple):
            return self.__class__(self.x - __value[0], self.y - __value[1])

        if isinstance(__value, (int, float)):
            return self.__class__(self.x - __value, self.y - __value)

        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __repr__(self) -> str:
        return f"{self.__class__}({self.x}, {self.y})"

    def convert(self) -> tuple[float, float]:
        return (self.x, self.y)
