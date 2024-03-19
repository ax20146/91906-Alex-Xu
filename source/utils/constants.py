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


class Duration: ...


class Speed: ...


class Health: ...


class Damage: ...


class Range: ...
