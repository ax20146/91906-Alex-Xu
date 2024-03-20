# Map Constants
TILE_SIZE = 64
MAP_WIDTH = 15
MAP_HEIGHT = 10


# Screen Constants
class Screen:
    TITLE = "Defender"
    WIDTH = MAP_WIDTH * TILE_SIZE
    HEIGHT = MAP_HEIGHT * TILE_SIZE
    SIZE = (WIDTH, HEIGHT)


class Layer:
    TILES = "Tiles"
    SLOTS = "Slots"
    WAYPOINTS = "Waypoints"
    DECORATIONS = "Decorations"
    PARTICLES = "Particles"
    COINS = "Coins"
    ENEMIES = "Enemies"
    TOWER = "Towers"


class Duration:
    SHORTEST = 50
    SHORTER = 150
    SHORT = 1000
    LONG = 2000
    LONGER = 5000
    LONGEST = 8000


class Speed:
    SLOW = 50
    MEDIUM = 100
    FAST = 150


class Health:
    LOW = 20
    MEDIUM = 50
    HIGH = 80


class Damage:
    LOW = 2
    MEDIUM = 25
    HIGH = 40


class Range:
    SHORT = 3 * TILE_SIZE
    FAR = 5 * TILE_SIZE


class Cooldown:
    SHORT = 150
    MEDIUM = 1000
    LONG = 2000


class Price:
    LOW = 25
    MEDIUM = 50
    HIGH = 80


class Value:
    LOW = 5
    HIGH = 20
