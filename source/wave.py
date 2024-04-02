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
    yield ("Wave 0", 15)
    yield 5000

    # Wave 1 Data
    yield ("Wave 1", 20)
    for _ in range(3):
        yield Soldier
        yield 1000
    yield 4000

    # Wave 2 Data
    yield ("Wave 2", 25)
    for _ in range(8):
        yield Soldier
        yield 1000
    yield 4000

    # Wave 3 Data
    yield ("Wave 3", 30)
    for _ in range(5):
        yield Zombie
        yield 400
    yield 4600

    # Wave 4 Data
    yield ("Wave 4", 35)
    for _ in range(5):
        yield Zombie
        yield 500
    for _ in range(10):
        yield Soldier
        yield 800
    yield 4200

    # Wave 5 Data
    yield ("Wave 5", 40)
    for _ in range(8):
        yield Knight
        yield 1500
    yield 6500

    # Wave 6 Data
    yield ("Wave 6", 50)
    for _ in range(10):
        yield Soldier
        yield 1000
    for _ in range(10):
        yield Knight
        yield 1000
    yield 7000

    # Wave 7 Data
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

    # Wave 8 Data
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

    # Wave 9 Data
    yield ("Wave 9", 100)
    for _ in range(20):
        yield Robot
        yield 1200
    for _ in range(25):
        yield Knight
        yield 800
    yield 9200

    # Wave 10 Data
    yield ("Wave 10", 120)
    for _ in range(50):
        yield Soldier
        yield 500
    for _ in range(35):
        yield Knight
        yield 800
    yield Tank
