# /utils/functions.py


# Import Built-In Dependencies
from math import cos, sin
from random import randint

# Import Local Dependencies
from .classes import Vector
from .constants import SCREEN_SIZE

__all__: list[str] = [
    "cos",
    "sin",
    "randrange",
    "limit_within",
]


def randrange(value: float, range: int) -> int:
    return randint(round(value) - range, round(value) + range)


def limit_within(
    point: Vector,
    *,
    lower: Vector = Vector(0, 0),
    upper: Vector = Vector(*SCREEN_SIZE)
) -> Vector:
    return Vector(
        min(max(point.x, lower.x), upper.x),
        min(max(point.y, lower.y), upper.y),
    )
