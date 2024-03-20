# /game.py

from typing import Iterator, TypeVar

import arcade

from .coins import Coin
from .enemies import Enemy, Knight, Robot, Soldier, Truck, Zombie
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
        self.window.show_view(Game())


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene
        self.clock: Clock
        self.timer: Timer

        self.select: Sprite | None = None
        self.hover: Sprite | None = None

        self.coin: int
        self.health: int

    def set_waypoints(self) -> Iterator[Point]:
        return (
            Point(*waypoint.position)
            for waypoint in sorted(
                self.scene["Waypoints"],
                key=lambda sprite: sprite.properties["tile_id"],
            )
        )

    def on_show_view(self) -> None:
        self.health = 10
        self.coin = 100

        self.clock = Clock()
        self.timer = Timer(2000, self.clock)

        self.scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap("./maps/Plains.tmx")
        )
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
            self.hover.on_select()  # type: ignore

        elif self.select:
            self.select.on_select()

        for i in self.scene["Enemies"]:
            if isinstance(i, Tank):
                i.turret.draw()

        arcade.draw_lrtb_rectangle_filled(0, 200, 64, 0, (0, 0, 0))
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

    def on_update(self, delta_time: float) -> None:
        if self.health <= 0:
            self.window.show_view(GameOver())

        self.clock.update(delta_time)
        self.scene.on_update(delta_time)
        self.health = Enemy.health

        if self.timer.available():
            self.timer.update()
            self.scene.add_sprite(
                "Enemies",
                rand_choice((Soldier, Zombie, Robot, Knight, Truck, Tank))(),
            )

        Tower.targets = self.scene.get_sprite_list("Enemies")
        Rocket.targets = self.scene.get_sprite_list("Enemies")
        TankCanon.targets = self.scene.get_sprite_list("Slots")

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
        if info := arcade.get_sprites_at_point((x, y), self.scene["Coins"]):
            coin: Coin = info[-1]  # type: ignore
            self.coin = coin.on_collect(self.coin)
            return

        if data := arcade.get_sprites_at_point((x, y), self.scene["Enemies"]):
            enemy: Enemy = data[-1]
            self.hover = enemy
            return

        self.hover = None
