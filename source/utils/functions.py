# /utils/functions.py


import arcade

from .classes.vector import Vector
from .constants import (
    HEALTH,
    INFO_UI_HEIGHT,
    INFO_UI_MARGIN,
    INFO_UI_WIDTH,
    LAYER_WAYPOINTS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SMALL_INFO_UI_WIDTH,
    UI_BACKGROUND_COLOUR,
    UI_HEALTHBAR_COLOUR,
)
from .types import Iterator

FONT = "Kenney Future Narrow"


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


def small_infobar(text: str, start_x: int):
    start_y: int = SCREEN_HEIGHT - INFO_UI_HEIGHT - INFO_UI_MARGIN
    end_x: int = start_x + SMALL_INFO_UI_WIDTH
    end_y: int = start_y - INFO_UI_HEIGHT

    arcade.draw_polygon_filled(
        color=UI_BACKGROUND_COLOUR,
        point_list=(
            (start_x, start_y),
            (end_x, start_y),
            (end_x - INFO_UI_MARGIN * 4, end_y),
            (start_x + INFO_UI_MARGIN * 4, end_y),
        ),
    )
    arcade.draw_text(
        text,
        (start_x + end_x) // 2,
        start_y - INFO_UI_HEIGHT // 2,
        font_name=FONT,
        anchor_x="center",
        anchor_y="center",
    )


def healthbar_draw(health: int) -> None:
    arcade.draw_rectangle_filled(
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - INFO_UI_HEIGHT // 2,
        width=INFO_UI_WIDTH,
        height=INFO_UI_HEIGHT,
        color=UI_BACKGROUND_COLOUR,
    )
    arcade.draw_rectangle_filled(
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - INFO_UI_HEIGHT // 2,
        width=(max(health, 0) / HEALTH) * (INFO_UI_WIDTH - INFO_UI_MARGIN),
        height=INFO_UI_HEIGHT - INFO_UI_MARGIN,
        color=UI_HEALTHBAR_COLOUR,
    )
    arcade.draw_text(
        f"{max(health, 0)} / {HEALTH}",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 2,
        font_name=FONT,
        anchor_x="center",
        anchor_y="top",
    )


def wavebar_draw(text: str) -> None:
    small_infobar(text, SCREEN_WIDTH // 5)


def coinbar_draw(coin: int) -> None:
    small_infobar(f"${coin:,}", 3 * SCREEN_WIDTH // 5)
