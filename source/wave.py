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
from .utils.types import Iterator, NamedTuple


# Define Wave data structure.
class Wave(NamedTuple):
    display: str
    coin: int


# Define Wave generator function
def wave() -> Iterator[type[Enemy] | Wave | int]:
    """`Wave` generator function.
    Yield different information regarding waves.

    Yields:
        Iterator[type[Enemy] | tuple[str, int] | int]:
        The wave generator `iterator` object yield:
            type[Enemy]: The enemy entity that should be spawned.
            tuple[str, int]: The display text & coin rewarded for wave.
            int: The time (in milliseconds) to delay the next yield.

    NOTE: The `wave` generator function contain many
    literal-strings, and 'arbitrary' integer values.
    However this approach of manually hand crafting each part of the
    game's progression allows finer control of the game's difficulty,
    whilst also allowing easier balancing changes made to the game.
    """

    # Wave 0 Data
    yield Wave("Wave 0", 25)
    yield 7500

    # Wave 1 Data
    yield Wave("Wave 1", 5)
    for _ in range(3):
        yield Soldier
        yield 1000
    yield 4000

    # Wave 2 Data
    yield Wave("Wave 2", 10)
    for _ in range(8):
        yield Soldier
        yield 800
    yield 4200

    # Wave 3 Data
    yield Wave("Wave 3", 15)
    for _ in range(5):
        yield Zombie
        yield 1000
    yield 4000

    # Wave 4 Data
    yield Wave("Wave 4", 20)
    for _ in range(4):
        yield Soldier
        yield 1200
    for _ in range(4):
        yield Zombie
        yield 800
    for _ in range(10):
        yield Soldier
        yield 750
    yield 4250

    # Wave 5 Data
    yield Wave("Wave 5", 25)
    for _ in range(10):
        yield Knight
        yield 2000
    yield 6000

    # Wave 6 Data
    yield Wave("Wave 6", 30)
    for _ in range(15):
        yield Soldier
        yield 500
    for _ in range(10):
        yield Knight
        yield 1000
    yield 7000

    # Wave 7 Data
    yield Wave("Wave 7", 35)
    for _ in range(12):
        yield Knight
        yield 500
    for _ in range(15):
        yield Zombie
        yield 750
    for _ in range(12):
        yield Knight
        yield 500
    yield 7500

    # Wave 8 Data
    yield Wave("Wave 8", 40)
    for _ in range(20):
        yield Soldier
        yield 500
    for _ in range(15):
        yield Robot
        yield 800
    yield 9200

    # Wave 9 Data
    yield Wave("Wave 9", 45)
    for _ in range(20):
        yield Robot
        yield 350
    for _ in range(20):
        yield Knight
        yield 750
    yield 9250

    # Wave 10 Data
    yield Wave("Wave 10", 50)
    for _ in range(20):
        yield Robot
        yield 1000
    for _ in range(30):
        yield Soldier
        yield 500
    yield Tank
