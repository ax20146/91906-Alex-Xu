# /source/utils.py


import arcade.arcade_types as arcade_types

# Define constants for screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


# Define constants for map layers
LAYER_WAYPOINTS = "Waypoints"
LAYER_BACKGROUND = "Background"
LAYER_PLACEABLE = "Placeable"


# Define types
ArcadePoint = arcade_types.Point


class Point:
    __slots__ = "x", "y"

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Point):
            return self.x == __value.x and self.y == __value.y

        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def round(self, n_digit: int = 0) -> "Point":
        return Point(round(self.x, n_digit), round(self.y, n_digit))

    def convert(self) -> tuple[float, float]:
        return (self.x, self.y)
