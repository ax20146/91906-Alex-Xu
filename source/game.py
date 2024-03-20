# /game.py

from typing import Iterator, TypeVar

import arcade

from .coins import Coin
from .enemies import Enemy, Knight, Robot, Soldier, Truck, Zombie
from .entities import Particle
from .towers import Canon, MachineGun, Tower
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
        arcade.Text(
            "Game Over", Screen.WIDTH // 2, Screen.HEIGHT // 2, font_size=40
        ).draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.window.show_view(Game())


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene
        self.clock: Clock
        self.timer: Timer

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

        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Particles")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Towers")

        Sprite.clock = self.clock
        Tower.lst = self.scene["Towers"]
        Coin.lst = self.scene["Coins"]
        Particle.lst = self.scene["Particles"]

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

        arcade.Text(f"Coin: {self.coin}", 100, 100).draw()
        arcade.Text(f"Health: {self.health}", 100, 150).draw()

    def on_update(self, delta_time: float) -> None:
        self.clock.update(delta_time)
        self.scene.on_update(delta_time)

        if self.timer.available():
            self.timer.update()
            self.scene.add_sprite(
                "Enemies",
                rand_choice((Soldier, Zombie, Robot, Knight, Truck))(),
            )

        Tower.targets = self.scene.get_sprite_list("Enemies")

        if self.health <= 0:
            self.window.show_view(GameOver())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if info := arcade.get_sprites_at_point((x, y), self.scene["Slots"]):
            slot: Sprite = info[-1]  # type: ignore
            slot.properties.setdefault("placed", False)

            if button == arcade.MOUSE_BUTTON_LEFT:
                tower = Canon(slot.position)
            else:
                tower = MachineGun(slot.position)

            if slot.properties["placed"] or self.coin - tower.price < 0:
                tower.kill()
                return

            self.coin -= tower.price

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if info := arcade.get_sprites_at_point((x, y), self.scene["Coins"]):
            coin: Coin = info[-1]  # type: ignore
            self.coin = coin.on_collect(self.coin)
