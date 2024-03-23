# /utils/functions.py


from math import atan2, cos, sin
from random import randint as _randint

__all__: list[str] = [
    "cos",
    "sin",
    "atan2",
    "randrange",
]


def randrange(value: float, range: int) -> int:
    return _randint(round(value) - range, round(value) + range)
