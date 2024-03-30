from typing import Any, Callable

import arcade
import arcade.gui

from . import menu
from .entities.entities.enemies import Enemy
from .entities.entities.entities import Entity
from .entities.entities.reinforcements import Reinforcement, Tank, Truck
from .entities.particles.coins import Coin
from .entities.particles.particles import Particle
from .entities.slots import Slot
from .entities.turrets.canons import TankCanon
from .entities.turrets.towers import Canon, MachineGun, RocketLauncher, Tower
from .utils import Clock, Sprite, Timer, Vector, functions
from .utils.functions import coinbar_draw, healthbar_draw, wavebar_draw
from .utils.types import Any
from .wave import wave

UI_TOWER_BTN = 0


class Btn(Sprite):
    def __init__(
        self,
        filename: str,
        position: Vector,
        click: type[Tower | Reinforcement],
    ) -> None:
        super().__init__(filename=filename, position=position)
        self.click: type[Tower | Reinforcement] = click

    def on_draw(self, **kwargs: Any) -> None:
        self.draw()  # type: ignore
        arcade.draw_text(
            str(self.click.PRICE),
            self.x,
            self.y - self.height // 3,
            font_name="Kenney Future Narrow",
            anchor_x="center",
            anchor_y="center",
        )


class Game(arcade.View):
    def __init__(self, map: str) -> None:
        super().__init__()

        self.map = map
        tilemap = arcade.load_tilemap(f"./maps/{map}.tmx")

        self.scene: arcade.Scene = arcade.Scene.from_tilemap(tilemap)

        self.clock: Clock = Clock()
        self.timer: Timer = Timer(self.clock, 0)

        self.select: Sprite | None = None
        self.hover: Sprite | None = None

        self.wave = wave()
        self.display: str = "Wave 0"
        self.health: int = 100
        self.coin: int = 10000

        for slot in (sprite for sprite in self.scene["Locations"]):
            self.scene.add_sprite("Slots", Slot(Vector(*slot.position)))

        self.scene.remove_sprite_list_by_name("Locations")
        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Towers")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Reinforcements")
        self.scene.add_sprite_list("Particles")

        self.scene.add_sprite(
            "UI",
            Btn(
                "./assets/UI/Gun.png",
                Vector(64, 240),
                MachineGun,
            ),
        )
        self.scene.add_sprite(
            "UI",
            Btn("./assets/UI/Canon.png", Vector(64, 152), Canon),
        )
        self.scene.add_sprite(
            "UI",
            Btn(
                "./assets/UI/Rocket.png",
                Vector(64, 64),
                RocketLauncher,
            ),
        )
        self.scene.add_sprite(
            "Troop UI",
            Btn(
                "./assets/UI/Truck.png",
                Vector(152, 64),
                Truck,
            ),
        )
        self.scene.add_sprite(
            "Troop UI",
            Btn(
                "./assets/UI/Tank.png",
                Vector(240, 64),
                Tank,
            ),
        )

        waypoints = tuple(functions.process_waypoints(tilemap))

        Sprite.clock = self.clock
        Enemy.sprite_list = self.scene["Enemies"]
        Enemy.targets = self.scene["Reinforcements"]
        Enemy.waypoints = waypoints

        Tank.timer = None
        Truck.timer = None
        Reinforcement.sprite_list = self.scene["Reinforcements"]
        Reinforcement.waypoints = tuple(reversed(waypoints))
        Reinforcement.targets = self.scene["Enemies"]

        Coin.sprite_list = self.scene["Coins"]
        Particle.sprite_list = self.scene["Particles"]
        Tower.sprite_list = self.scene["Towers"]
        Tower.targets = self.scene["Enemies"]

    def on_draw(self):
        self.clear()
        self.scene.draw()  # type: ignore

        coinbar_draw(self.coin)
        wavebar_draw(self.display)
        healthbar_draw(self.health)

        if self.hover and isinstance(self.hover, (Entity, Slot)):
            self.hover.on_hover_draw()

        if self.select and isinstance(self.select, Entity):
            if (
                self.select in self.scene["Enemies"]
                or self.select in self.scene["Reinforcements"]
            ):
                self.select.on_hover_draw()
            else:
                self.select = None

        if self.select and isinstance(self.select, Slot):
            if self.select.turret:
                arcade.draw_circle_filled(
                    *self.select.xy.convert(),
                    radius=self.select.turret.range,
                    color=(0, 0, 0, 80),
                )
                self.select.on_hover_draw()
            else:
                self.select.draw_hit_box(line_thickness=2)
                for i in self.scene["UI"]:
                    if isinstance(i, Btn):
                        if i.click.affordable(self.coin):
                            i.alpha = 255
                        else:
                            i.alpha = 100
        else:
            for i in self.scene["UI"]:
                i.alpha = 100

        for i in self.scene["UI"]:
            if isinstance(i, Btn):
                i.on_draw()

        for i in self.scene["Troop UI"]:
            if isinstance(i, Btn):
                i.on_draw()
                if i.click.affordable(self.coin):
                    i.alpha = 255
                else:
                    i.alpha = 100

    def on_update(self, delta_time: float) -> None:
        if self.health <= 0:
            self.window.show_view(menu.Defeat())
            return
        elif len(self.scene["Enemies"]) == 0 and self.timer.duration < 0:
            self.window.show_view(menu.Victory(self.map))
            return

        self.clock.update(delta_time)
        self.scene.update()

        for sprite in (
            sprite
            for sprite in self.scene["Enemies"]
            if isinstance(sprite, Enemy) and sprite.is_end()
        ):
            self.health -= sprite.on_end()

        if not self.timer.available():
            return

        try:
            wave_info = next(self.wave)
        except StopIteration:
            self.timer.duration = -1
            return

        if isinstance(wave_info, int):
            self.timer.duration = wave_info
            return
        elif isinstance(wave_info, str):
            self.display = wave_info
            self.coin += int(wave_info[-2:]) * 10
        else:
            wave_info()

        self.timer.duration = 0
        self.timer.update()

    def on_mouse_press(self, x: int, y: int, button: int, *args: Any) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if a := arcade.get_sprites_at_point(
                (x, y), self.scene["Troop UI"]
            ):
                if (
                    isinstance(a[-1], Btn)
                    and issubclass(a[-1].click, Reinforcement)
                    and a[-1].click.affordable(self.coin)
                ):
                    a[-1].click()
                    a[-1].click.timer.update()
                    self.coin -= a[-1].click.PRICE
                    return

            if (
                self.select
                and isinstance(self.select, Slot)
                and (
                    a := arcade.get_sprites_at_point((x, y), self.scene["UI"])
                )
                and not self.select.turret
            ):
                if (
                    isinstance(a[-1], Btn)
                    and issubclass(a[-1].click, Tower)
                    and a[-1].click.affordable(self.coin)
                ):
                    self.select.turret = a[-1].click(self.select.xy)
                    self.coin -= self.select.turret.PRICE

            self.on_select((x, y))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if (
                (
                    s := arcade.get_sprites_at_point(
                        (x, y), self.scene["Slots"]
                    )
                )
                and isinstance(s[-1], Slot)
                and s[-1].turret
            ):
                self.coin += s[-1].turret.on_sell()
                s[-1].turret = None
            self.select = None

    def on_select(self, xy: tuple[int, int]):
        if (
            select := self.mouse_over(xy, self.scene["Slots"])
            or (select := self.mouse_over(xy, self.scene["Enemies"]))
            or (select := self.mouse_over(xy, self.scene["Reinforcements"]))
        ):
            self.select = select
            return

        self.select = None

    def on_mouse_motion(self, x: int, y: int, *args: Any) -> None:
        self.on_hover((x, y))
        if a := arcade.get_sprites_at_point((x, y), self.scene["Coins"]):
            if isinstance(a[-1], Coin):
                self.coin += a[-1].on_collect()

    def on_hover(self, xy: tuple[int, int]) -> None:
        if (
            (hover := self.mouse_over(xy, self.scene["Slots"]))
            or (hover := self.mouse_over(xy, self.scene["Enemies"]))
            or (hover := self.mouse_over(xy, self.scene["Reinforcements"]))
        ):
            self.hover = hover
            return

        self.hover = None

    @staticmethod
    def mouse_over(
        xy: tuple[int, int], lst: arcade.SpriteList
    ) -> Sprite | None:
        if sprites := [
            sprite
            for sprite in arcade.get_sprites_at_point(xy, lst)
            if isinstance(sprite, Sprite)
        ]:
            if len(sprites) >= 2 and isinstance(sprites[-1], TankCanon):
                return sprites[-2]
            return sprites[-1]
