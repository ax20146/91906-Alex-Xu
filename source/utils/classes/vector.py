# /utils/classes/vector.py


# Import Built-In Dependencies
from math import hypot


# Define Vector Class
class Vector:
    __slots__ = "x", "y"

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented

        return self.x == __value.x and self.y == __value.y

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def __add__(self, __value: "Vector") -> "Vector":
        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: "Vector") -> "Vector":
        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __mul__(self, __value: float) -> "Vector":
        return self.__class__(self.x * __value, self.y * __value)

    def __truediv__(self, __value: float) -> "Vector":
        return self.__class__(self.x / __value, self.y / __value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def normalise(self) -> "Vector":
        return self / abs(self)

    def length(self) -> float:
        return abs(self)

    def convert(self) -> tuple[float, float]:
        return (self.x, self.y)
