# source/wave.py

from .entities.entities.enemies import (
    Enemy,
    Knight,
    Robot,
    Soldier,
    Tank,
    Zombie,
)
from .utils.types import Iterator


def wave() -> Iterator[type[Enemy] | str | int]:
    yield "Wave 0"
    yield 3000

    yield "Wave 1"
    for _ in range(3):
        yield Soldier
        yield 1000
    yield 7000

    yield "Wave 2"
    for _ in range(10):
        yield Soldier
        yield 800
    yield 7200

    yield "Wave 3"
    for _ in range(5):
        yield Zombie
        yield 500
    yield 9500

    yield "Wave 4"
    for _ in range(8):
        yield Zombie
        yield 1000
    for _ in range(15):
        yield Soldier
        yield 800
    yield 9200

    yield "Wave 5"
    for _ in range(8):
        yield Knight
        yield 2000
    yield 10000

    yield "Wave 6"
    for _ in range(10):
        yield Soldier
        yield 1000
    for _ in range(10):
        yield Knight
        yield 1500
    yield 10500

    yield "Wave 7"
    for _ in range(8):
        yield Zombie
        yield 500
    for _ in range(15):
        yield Soldier
        yield 800
    for _ in range(10):
        yield Knight
        yield 1000
    yield 10500

    yield "Wave 8"
    for _ in range(25):
        yield Soldier
        yield 1000
    for _ in range(10):
        yield Robot
        yield 1500
    yield 13500

    yield "Wave 9"
    for _ in range(25):
        yield Robot
        yield 1200
    for _ in range(25):
        yield Knight
        yield 1500
    yield 13500

    yield "Wave 10"
    yield Tank
