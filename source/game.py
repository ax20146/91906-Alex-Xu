# /game.py

from math import atan2, cos, sin
from typing import Iterator, NamedTuple, TypeVar

import arcade

from .coins import Coin
from .enemies import Enemies, Enemy, Soldier, Zombie
from .entities import Particle
from .slots import Slot
from .tank import Tank, TankCanon
from .towers import Canon, MachineGun, Rocket, RocketLauncher, Tower
from .utils import Clock, Point, Sprite, Timer
from .utils.constants import Screen

_T = TypeVar("_T")


def rand_choice(choices: list[_T] | tuple[_T, ...]) -> _T:
    from random import choice

    return choice(choices)


class WaveInfo(NamedTuple):
    enemy: Enemies
    delay: int


def wave() -> Iterator[WaveInfo | None]:
    for _ in range(5):
        yield WaveInfo(Soldier, 500)

    yield None

    for _ in range(3):
        yield WaveInfo(Zombie, 1000)

    for _ in range(5):
        yield WaveInfo(Soldier, 500)


class GameOver(arcade.View):
    def __init__(self) -> None:
        super().__init__()

    def on_draw(self):
        arcade.draw_rectangle_filled(
            Screen.WIDTH // 2, Screen.HEIGHT // 2, 500, 128, (0, 0, 0)
        )
        arcade.draw_text(
            "Game Over",
            Screen.WIDTH // 2,
            Screen.HEIGHT // 2,
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            color=(200, 100, 100),
        )

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        from .menu import Menu

        self.window.show_view(Menu())


class Game(arcade.View):
    def __init__(self, map: str) -> None:
        super().__init__()

        self.scene: arcade.Scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap(map)
        )
        self.clock: Clock = Clock()
        self.timer: Timer = Timer(1, self.clock)

        self.select: Sprite | None = None
        self.hover: Sprite | None = None

        self.coin: int = 100
        self.wave: Iterator[WaveInfo | None] | None = wave()
        self.wave_num: int = 1
        self.health: int = 10

    def set_waypoints(self) -> Iterator[Point]:
        return (
            Point(*waypoint.position)
            for waypoint in sorted(
                self.scene["Waypoints"],
                key=lambda sprite: sprite.properties["tile_id"],
            )
        )

    def on_show_view(self) -> None:
        Enemy.waypoints = tuple(self.set_waypoints())

        for slot in self.scene["Locations"]:
            self.scene.add_sprite(
                "Slots", Slot((slot.center_x, slot.center_y))
            )

        self.scene.remove_sprite_list_by_name("Locations")
        self.scene.remove_sprite_list_by_name("Waypoints")

        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Towers")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Particles")
        self.scene.add_sprite_list("UI")

        Sprite.clock = self.clock
        Tower.lst = self.scene["Towers"]
        Coin.lst = self.scene["Coins"]
        Particle.lst = self.scene["Particles"]
        Enemy.health = self.health
        Rocket.lst = self.scene["Particles"]

    def on_draw(self) -> None:
        self.clear()
        self.scene.draw()  # type: ignore

        if isinstance(self.select, Enemy):
            self.select = None if self.select.health <= 0 else self.select

        if self.hover and not self.select:
            self.hover.on_select_draw()  # type: ignore

        elif self.select:
            self.select.on_select_draw()  # type: ignore

        for i in self.scene["Enemies"]:
            if isinstance(i, Tank):
                i.turret.draw()  # type: ignore

        arcade.draw_lrtb_rectangle_filled(0, 200, 92, 0, (0, 0, 0))
        arcade.draw_text(
            f"Coins: {self.coin}",
            width=150,
            anchor_y="center",
            font_size=16,
            start_x=25,
            start_y=25,
        )
        arcade.draw_text(
            f"Health: {self.health}",
            width=150,
            anchor_y="center",
            font_size=16,
            start_x=25,
            start_y=50,
        )
        arcade.draw_text(
            f"Wave: {self.wave_num}",
            width=150,
            anchor_y="center",
            font_size=16,
            start_x=25,
            start_y=75,
        )

    def on_update(self, delta_time: float) -> None:
        if self.health <= 0 or (
            self.wave is None and not len(self.scene["Enemies"])
        ):
            self.window.show_view(GameOver())

        self.clock.update(delta_time)
        self.scene.on_update(delta_time)
        self.health = Enemy.health

        Tower.targets = self.scene.get_sprite_list("Enemies")
        Rocket.targets = self.scene.get_sprite_list("Enemies")
        TankCanon.targets = self.scene.get_sprite_list("Slots")

        if self.timer.available():
            try:
                wave_data = next(self.wave)
            except StopIteration:
                self.timer.delay = 0
                self.wave = None
                return

            if wave_data is None:
                self.wave_num += 1
                self.timer.delay = 10000
                self.timer.update()
                return

            enemy, delay = wave_data

            self.scene.add_sprite("Enemies", enemy())
            self.timer.delay = delay
            self.timer.update()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if data := arcade.get_sprites_at_point((x, y), self.scene["Enemies"]):
            self.select = data[-1]  # type:ignore
            return

        if (
            data := arcade.get_sprites_at_point((x, y), self.scene["Slots"])
        ) and not self.select:
            slot: Slot = data[-1]  # type: ignore

            if button == arcade.MOUSE_BUTTON_LEFT and not slot.turret:
                tower = Canon(slot.position)
            elif button == arcade.MOUSE_BUTTON_MIDDLE and not slot.turret:
                tower = RocketLauncher(slot.position)
            elif button == arcade.MOUSE_BUTTON_RIGHT and not slot.turret:
                tower = MachineGun(slot.position)
            elif button == arcade.MOUSE_BUTTON_RIGHT and slot.turret:
                self.coin += slot.turret.price // 2
                slot.turret.kill()
                slot.turret = None
                self.select = None
                return
            else:
                self.select = slot
                return

            if slot.turret or self.coin - tower.price < 0:
                tower.kill()
                return

            self.coin -= tower.price
            slot.turret = tower

        self.select = None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        coin: Coin
        for coin in self.scene["Coins"]:  # type: ignore
            p = Point(*coin.position)
            p2 = Point(x, y)

            if p.within(p2, range=64):
                angle: float = -atan2(x - p.x, y - p.y)

                coin.x -= 1 * sin(angle)
                coin.y += 1 * cos(angle)

        if info := arcade.get_sprites_at_point((x, y), self.scene["Coins"]):
            coin: Coin = info[-1]  # type: ignore
            self.coin = coin.on_collect(self.coin)
            return

        if data := arcade.get_sprites_at_point((x, y), self.scene["Enemies"]):
            enemy: Enemy = data[-1]  # type: ignore
            self.hover = enemy
            return

        self.hover = None
