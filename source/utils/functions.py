# /utils/functions.py


from math import atan2, cos, sin
from random import randint as _randint

from .classes import Point
from .constants import SCREEN_SIZE

__all__: list[str] = [
    "cos",
    "sin",
    "atan2",
    "randrange",
]


def randrange(value: float, range: int) -> int:
    return _randint(round(value) - range, round(value) + range)


def limit_within(
    point: Point,
    *,
    lower: Point = Point(0, 0),
    upper: Point = Point(*SCREEN_SIZE)
) -> Point:
    return Point(
        min(max(point.x, lower.x), upper.x),
        min(max(point.y, lower.y), upper.y),
    )
