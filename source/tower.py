# /source/tower.py


import arcade

from .enemy import Enemy
from .utils.constants import COOLDOWN_MEDIUM, DAMAGE_MEDIUM, RANGE_MEDIUM
from .utils.types import ClassVar


class Tower(arcade.Sprite):
    targets: ClassVar[arcade.SpriteList]

    def __init__(self, assets: str | None = None) -> None:
        super().__init__(
            ":resources:images/topdown_tanks/tankBody_dark.png"
            if assets is None
            else assets
        )

        self.target: Enemy | None = None

        self.damage: int = DAMAGE_MEDIUM
        self.range: int = RANGE_MEDIUM

        self.current_time: float = 0
        self.previous_time: float = 0
        self.cooldown_time: float = COOLDOWN_MEDIUM / 1000

    @property
    def cooldown(self) -> bool:
        return self.current_time - self.previous_time < self.cooldown_time

    def choose_target(self) -> None:
        if (info := arcade.get_closest_sprite(self, self.targets)) is None:
            self.target = None
            return

        target, distance = info
        if not isinstance(target, Enemy) or distance > self.range:
            self.target = None
            return

        self.target = target

    def attack(self) -> None:
        if self.target is None:
            return

        self.target.health -= self.damage
        print(self.target.health)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        # Update Timer
        self.current_time += delta_time

        # Select Target
        self.choose_target()
        if self.target is None:
            return

        self.face_point(self.target.position)

        # Cooldown
        if self.cooldown:
            return
        self.previous_time = self.current_time

        # Attack
        self.attack()
