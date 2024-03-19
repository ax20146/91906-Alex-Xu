# /game.py

from random import choice
from typing import Iterator, TypeVar

import arcade

from .coins import Coin
from .enemy import Enemy, Knight, Robot, Soldier, Truck, Zombie
from .entity import TurretEntity
from .tower import Canon
from .utils import SCREEN_HEIGHT, SCREEN_WIDTH, Clock, Sprite, Vector

_T = TypeVar("_T")


def rand_choice(choices: list[_T] | tuple[_T, ...]) -> _T:
    return choice(choices)


class Timer:
    __slots__ = ("previous", "delay")

    def __init__(self, delay: int = 0) -> None:
        self.previous: float = 0
        self.delay: int = delay

    def available(self, time: float) -> bool:
        return time - self.previous >= self.delay


class GameOver(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

    def on_draw(self):
        self.clear()

        text = arcade.Text("Game Over", 0, 0)
        text.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        text.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.window.show_view(Game())


class MenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

    def on_draw(self):
        self.clear()

        text = arcade.Text("Game Over", 0, 0)
        text.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        text.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.window.show_view(Game())


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.scene: arcade.Scene

        self.coin: int
        self.health: int
        self.clock: Clock
        self.timer: Timer

    def set_waypoints(self) -> Iterator[Vector]:
        return (
            Vector(*waypoint.position)
            for waypoint in sorted(
                self.scene["Waypoints"],
                key=lambda sprite: sprite.properties["tile_id"],
            )
        )

    def on_show_view(self) -> None:
        self.health = 10
        self.coin = 100

        self.clock = Clock()
        self.timer = Timer(2000)

        self.scene = arcade.Scene.from_tilemap(
            arcade.load_tilemap("./maps/Plains.tmx")
        )
        Enemy.waypoints = tuple(self.set_waypoints())

        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Particles")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Towers")

        Sprite.clock = self.clock
        Enemy.health = self.health
        Enemy.coin_list = self.scene["Coins"]
        Coin.amount = self.coin

    def on_draw(self) -> None:
        self.clear()

        self.scene.draw()  # type: ignore

        arcade.Text(f"Coin: {self.coin}", 100, 100).draw()
        arcade.Text(f"Health: {self.health}", 100, 150).draw()

    def on_update(self, delta_time: float) -> None:
        self.clock.update(delta_time)
        self.scene.on_update(delta_time)
        self.health = Enemy.health
        self.coin = Coin.amount

        if self.timer.available(self.clock.time):
            self.timer.previous = self.clock.time
            self.scene.add_sprite(
                "Enemies",
                rand_choice((Soldier, Zombie, Robot, Knight, Truck))(),
            )

        TurretEntity.targets = self.scene.get_sprite_list("Enemies")
        TurretEntity.particles = self.scene.get_sprite_list("Particles")

        if self.health <= 0:
            self.window.show_view(GameOver())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.on_left_mouse_press(x, y)

        # print(self.scene["Slots"].properties)

        # if info := arcade.get_sprites_at_point((x, y), self.scene["Slots"]):
        #     slot: arcade.Sprite = info[-1]

        #     slot.properties.setdefault("placed", False)

        #     print(slot.properties)
        #     if slot.properties["placed"]:
        #         return

        #     self.scene.add_sprite(
        #         "Tower", Canon((slot.center_x, slot.center_y))
        #     )
        #     slot.properties["placed"] = True

        # if arcade.get_sprites_at_point(
        #     (x, y), self.scene.get_sprite_list("Tiles")
        # ):
        #     print("hi")
        #     self.scene.add_sprite("Enemy", Soldier())

    def on_left_mouse_press(self, x: int, y: int):
        if info := arcade.get_sprites_at_point((x, y), self.scene["Slots"]):
            slot = info[0]

            if not hasattr(slot, "tower"):
                setattr(slot, "tower", None)

            if slot.tower is not None:
                return

            tower = Canon((slot.center_x, slot.center_y))
            if self.coin - tower.price < 0:
                return

            Coin.amount -= tower.price
            slot.tower = tower
            self.scene.add_sprite("Towers", tower)

        if info := arcade.get_sprites_at_point((x, y), self.scene["Tiles"]):
            self.scene.add_sprite("Enemies", Soldier())

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if info := arcade.get_sprites_at_point((x, y), self.scene["Coins"]):
            coin: Coin = info[-1]  # type: ignore
            coin.on_collect()

        if info := arcade.get_sprites_at_point((x, y), self.scene["Enemies"]):
            enemy: Enemy = info[-1]  # type: ignore

            # Display
            print(enemy.health, enemy.speed)

        if info := arcade.get_sprites_at_point((x, y), self.scene["Towers"]):
            tower: TurretEntity = info[-1]  # type: ignore

            # Display
            print(tower.damage, tower.range)
