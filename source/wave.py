# /wave.py
"""`Wave` module containing the wave generator function."""


# Import Local Dependencies
from .entities.entities.enemies import (
    Enemy,
    Knight,
    Robot,
    Soldier,
    Tank,
    Zombie,
)
from .utils.types import Iterator


# Define Wave generator function
def wave() -> Iterator[type[Enemy] | tuple[str, int] | int]:
    yield ("Wave 0", 15)
    yield 5000

    yield ("Wave 1", 20)
    for _ in range(3):
        yield Soldier
        yield 1000
    yield 4000

    yield ("Wave 2", 25)
    for _ in range(8):
        yield Soldier
        yield 1000
    yield 4000

    yield ("Wave 3", 30)
    for _ in range(5):
        yield Zombie
        yield 400
    yield 4600

    yield ("Wave 4", 35)
    for _ in range(5):
        yield Zombie
        yield 500
    for _ in range(10):
        yield Soldier
        yield 800
    yield 4200

    yield ("Wave 5", 40)
    for _ in range(8):
        yield Knight
        yield 1500
    yield 6500

    yield ("Wave 6", 50)
    for _ in range(10):
        yield Soldier
        yield 1000
    for _ in range(10):
        yield Knight
        yield 1000
    yield 7000

    yield ("Wave 7", 60)
    for _ in range(15):
        yield Zombie
        yield 250
    for _ in range(15):
        yield Soldier
        yield 500
    for _ in range(12):
        yield Knight
        yield 800
    yield 7200

    yield ("Wave 8", 80)
    for _ in range(25):
        yield Zombie
        yield 500
    for _ in range(25):
        yield Soldier
        yield 800
    for _ in range(8):
        yield Robot
        yield 1000
    yield 9000

    yield ("Wave 9", 100)
    for _ in range(20):
        yield Robot
        yield 1200
    for _ in range(25):
        yield Knight
        yield 800
    yield 9200

    yield ("Wave 10", 120)
    for _ in range(50):
        yield Soldier
        yield 500
    for _ in range(35):
        yield Knight
        yield 800
    yield Tank
