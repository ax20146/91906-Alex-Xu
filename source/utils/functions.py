# /utils/functions.py


import arcade

from .classes.vector import Vector
from .constants import LAYER_WAYPOINTS
from .types import Iterator


def process_pascal_case(string: str) -> str:
    result: str = string[0]

    for char in string[1:]:
        result += f" {char}" if char.isupper() else char

    return result


def process_waypoints(tilemap: arcade.TileMap) -> Iterator[Vector]:
    return (
        Vector(*waypoint)
        for waypoint in tilemap.object_lists[LAYER_WAYPOINTS][0].shape
        if isinstance(waypoint, tuple)
    )
