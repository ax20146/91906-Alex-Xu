# /utils/classes/vector.py


from ..functions import dataclass, hypot, randint


@dataclass(frozen=True, slots=True, repr=False)
class Vector:
    x: float = 0
    y: float = 0

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, __value: "Vector") -> "Vector":
        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: "Vector") -> "Vector":
        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __mul__(self, __value: float) -> "Vector":
        return self.__class__(self.x * __value, self.y * __value)

    def __truediv__(self, __value: float) -> "Vector":
        return self.__class__(self.x / __value, self.y / __value)

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def normalise(self) -> "Vector":
        return self / abs(self)

    def length(self) -> float:
        return abs(self)

    def randomise(self, range: int = 0) -> "Vector":
        return self.__class__(
            randint(round(self.x) - range, round(self.x) + range),
            randint(round(self.y) - range, round(self.y) + range),
        )

    def limit(self, lower: "Vector", upper: "Vector") -> "Vector":
        return self.__class__(
            min(max(self.x, lower.x), upper.x),
            min(max(self.y, lower.y), upper.y),
        )

    def within(self, vector: "Vector", range: float) -> bool:
        return (self - vector).length() <= range

    def convert(self) -> tuple[float, float]:
        return (self.x, self.y)
