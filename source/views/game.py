# /views/game.py


# Import 3rd-Party Dependencies
import arcade

from ..entities.buttons import Button

# Import Local Dependencies
from ..entities.entities.enemies import Enemy
from ..entities.entities.entities import Entity
from ..entities.entities.reinforcements import Reinforcement, reinforcements
from ..entities.entities.tanks import Canon
from ..entities.particles.coins import Coin
from ..entities.particles.particles import Particle
from ..entities.slots import Slot
from ..entities.turrets.towers import Tower, towers
from ..utils import Clock, Sprite, Timer, Vector, View
from ..utils.constants import (
    ANCHOR_CENTER,
    FONT,
    FONT_MEDIUM,
    GAMEPLAY_COIN,
    GAMEPLAY_HEALTH,
    HEALTHBAR_COLOUR,
    INFO_UI_FULL_H,
    INFO_UI_FULL_W,
    INFO_UI_HALF_H,
    INFO_UI_HEIGHT,
    INFO_UI_MARGIN,
    INFO_UI_SMALL_WIDTH,
    INFO_UI_WIDTH,
    LAYER_COINS,
    LAYER_ENEMIES,
    LAYER_LOCATIONS,
    LAYER_PARTICLES,
    LAYER_REINFORCEMENTS,
    LAYER_SLOTS,
    LAYER_TOWERS,
    LAYER_UI,
    LAYER_WAYPOINTS,
    SCREEN_HALF_W,
    SCREEN_HEIGHT,
    TILE_SIZE,
    TRANSPARENT_DARK,
    WHITE,
)
from ..utils.types import Any, Iterator, Type
from ..wave import wave
from . import endscreens


class Game(View):
    def __init__(self, tilemap: str) -> None:
        super().__init__()

        self.map: tuple[str, arcade.TileMap] = (
            tilemap,
            arcade.load_tilemap(f"./maps/{tilemap}.tmx"),
        )

        self.scene: arcade.Scene = arcade.Scene.from_tilemap(self.map[1])
        self.clock: Clock = Clock()
        self.timer: Timer = Timer(self.clock)

        self.select: Sprite | None = None
        self.hover: Sprite | None = None

        self.wave = wave()
        self.display: str = ""
        self.health: int = GAMEPLAY_HEALTH
        self.coin: int = GAMEPLAY_COIN

        self.process_locations()
        self.setup_scene()
        self.setup_classes()
        self.setup_ui()

    @staticmethod
    def process_waypoints(tilemap: arcade.TileMap) -> Iterator[Vector]:
        return (
            Vector(*waypoint)
            for waypoint in tilemap.object_lists[LAYER_WAYPOINTS][0].shape
            if isinstance(waypoint, tuple)
        )

    def process_locations(self) -> None:
        for slot in self.scene[LAYER_LOCATIONS]:
            self.scene.add_sprite(LAYER_SLOTS, Slot(Vector(*slot.position)))

    def setup_scene(self) -> None:
        self.scene.remove_sprite_list_by_name(LAYER_LOCATIONS)

        self.scene.add_sprite_list(LAYER_COINS)
        self.scene.add_sprite_list(LAYER_TOWERS)
        self.scene.add_sprite_list(LAYER_ENEMIES)
        self.scene.add_sprite_list(LAYER_REINFORCEMENTS)
        self.scene.add_sprite_list(LAYER_PARTICLES)

    def setup_classes(self) -> None:
        Sprite.clock = self.clock

        Enemy.waypoints = tuple(self.process_waypoints(self.map[1]))
        Enemy.sprite_list = self.scene[LAYER_ENEMIES]
        Enemy.targets = self.scene[LAYER_REINFORCEMENTS]

        Reinforcement.waypoints = tuple(reversed(Enemy.waypoints))
        Reinforcement.sprite_list = self.scene[LAYER_REINFORCEMENTS]
        Reinforcement.targets = self.scene[LAYER_ENEMIES]

        Tower.sprite_list = self.scene[LAYER_TOWERS]
        Tower.targets = self.scene[LAYER_ENEMIES]

        Slot.sprite_list = self.scene[LAYER_SLOTS]
        Coin.sprite_list = self.scene[LAYER_COINS]
        Particle.sprite_list = self.scene[LAYER_PARTICLES]

    def setup_ui(self) -> None:
        for idx, (obj, path) in enumerate(towers.items(), start=1):
            position = Vector(TILE_SIZE, TILE_SIZE * (9 * idx - 1) // 8)
            self.scene.add_sprite(LAYER_UI, Button(path, position, obj))

        for idx, (obj, path) in enumerate(reinforcements.items(), start=2):
            position = Vector(TILE_SIZE * (9 * idx - 1) // 8, TILE_SIZE)
            self.scene.add_sprite(LAYER_UI, Button(path, position, obj))

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()  # type: ignore

        self.draw_healthbar()
        self.draw_infobar(f"${self.coin:,}", INFO_UI_WIDTH)
        self.draw_infobar(self.display, INFO_UI_SMALL_WIDTH)

        if self.hover and isinstance(self.hover, (Entity, Slot, Button)):
            self.hover.on_hover_draw()

        if isinstance(self.select, (Entity, Slot)) and (
            self.select in self.scene[LAYER_SLOTS]
            or self.select in self.scene[LAYER_ENEMIES]
            or self.select in self.scene[LAYER_REINFORCEMENTS]
        ):
            self.select.on_select_draw()
        else:
            self.select = None

        for sprite in (
            sprite
            for sprite in self.scene[LAYER_UI]
            if isinstance(sprite, Button)
        ):
            sprite.on_draw()

    def draw_healthbar(self) -> None:
        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HALF_H,
            width=INFO_UI_FULL_W,
            height=INFO_UI_FULL_H,
            color=TRANSPARENT_DARK,
        )
        arcade.draw_rectangle_filled(
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HALF_H,
            width=(max(self.health, 0) / GAMEPLAY_HEALTH) * INFO_UI_WIDTH,
            height=INFO_UI_HEIGHT,
            color=HEALTHBAR_COLOUR,
        )
        arcade.draw_text(
            f"{max(self.health, 0)} / {GAMEPLAY_HEALTH}",
            SCREEN_HALF_W,
            SCREEN_HEIGHT - INFO_UI_HEIGHT // 2,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def draw_infobar(self, text: str, start_x: int) -> None:
        end_x = start_x + INFO_UI_SMALL_WIDTH
        start_y = SCREEN_HEIGHT - INFO_UI_FULL_H - INFO_UI_MARGIN
        end_y = start_y - INFO_UI_FULL_H

        arcade.draw_polygon_filled(
            color=TRANSPARENT_DARK,
            point_list=(
                (start_x, start_y),
                (end_x, start_y),
                (end_x - INFO_UI_MARGIN * 4, end_y),
                (start_x + INFO_UI_MARGIN * 4, end_y),
            ),
        )

        arcade.draw_text(
            text,
            start_x=(start_x + end_x) // 2,
            start_y=start_y - INFO_UI_HALF_H,
            font_name=FONT,
            font_size=FONT_MEDIUM,
            anchor_x=ANCHOR_CENTER,
            anchor_y=ANCHOR_CENTER,
            color=WHITE,
        )

    def on_update(self, delta_time: float) -> None:
        self.clock.update(delta_time)
        self.scene.update()

        self.update_state()
        self.update_wave()
        self.update_health()

        Button.update_data(self.coin, self.select)

    def update_state(self) -> None:
        if self.health <= 0:
            self.on_draw()
            self.window.show_view(endscreens.Defeat())
            return

        if self.timer.disable and not len(self.scene[LAYER_ENEMIES]):
            self.on_draw()
            self.window.show_view(endscreens.Victory(self.map[0]))
            return

    def update_health(self) -> None:
        for sprite in (
            sprite
            for sprite in self.scene[LAYER_ENEMIES]
            if isinstance(sprite, Enemy) and sprite.is_end()
        ):
            self.health -= sprite.on_end()

    def update_wave(self) -> None:
        if not self.timer.available():
            return

        try:
            wave_data = next(self.wave)
        except StopIteration:
            self.timer.disable = True
            return

        if isinstance(wave_data, int):
            self.timer.duration = wave_data
            return

        if isinstance(wave_data, tuple):
            self.display = wave_data[0]
            self.coin += wave_data[1]
        else:
            wave_data()

        self.timer.duration = 0
        self.timer.update()

    def on_mouse_press(self, x: int, y: int, button: int, *args: Any) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.on_mouse_left(x, y)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.on_mouse_right(x, y)

    def on_mouse_left(self, x: int, y: int) -> None:
        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_UI], type=Button
        ):
            self.coin -= sprite.on_click()
            return

        self.on_select((x, y))

    def on_mouse_right(self, x: int, y: int) -> None:
        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_SLOTS], type=Slot
        ):
            self.coin += sprite.on_sell()

    def on_select(self, xy: tuple[int, int]) -> None:
        self.select = (
            self.mouse_over(xy, self.scene[LAYER_SLOTS])
            or self.mouse_over(xy, self.scene[LAYER_REINFORCEMENTS])
            or self.mouse_over(xy, self.scene[LAYER_ENEMIES])
        )

    def on_mouse_motion(self, x: int, y: int, *args: Any) -> None:
        self.on_hover((x, y))

        Coin.target = Vector(x, y)

        if sprite := self.mouse_over(
            (x, y), self.scene[LAYER_COINS], type=Coin
        ):
            self.coin += sprite.on_collect()

    def on_hover(self, xy: tuple[int, int]) -> None:
        self.hover = (
            self.mouse_over(xy, self.scene[LAYER_UI])
            or self.mouse_over(xy, self.scene[LAYER_SLOTS])
            or self.mouse_over(xy, self.scene[LAYER_ENEMIES])
            or self.mouse_over(xy, self.scene[LAYER_REINFORCEMENTS])
        )

    @staticmethod
    def mouse_over(
        xy: tuple[int, int],
        lst: arcade.SpriteList,
        *,
        type: type[Type] = Sprite,
    ) -> Type | None:
        sprites: list[Type] = [
            sprite
            for sprite in arcade.get_sprites_at_point(xy, lst)
            if isinstance(sprite, type)
        ]

        if not sprites:
            return

        print(sprites)

        if isinstance(sprites[-1], Canon) and len(sprites) >= 2:
            return sprites[-2]
        return sprites[-1]
