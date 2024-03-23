# /utils/classes/vector.py


# Import Built-In Dependencies
from dataclasses import dataclass
from math import hypot


# Define Vector Class
@dataclass(frozen=True, slots=True)
class Vector:
    x: float = 0
    y: float = 0

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

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

    def normalise(self) -> "Vector":
        return self / abs(self)

    def length(self) -> float:
        return abs(self)

    def convert(self) -> tuple[float, float]:
        return (self.x, self.y)
