# /utils/classes/movement.py

from .sprite import Sprite
from .vector import Vector


class Movement:
    __slots__ = "_target", "_speed", "_sprite"

    def __init__(
        self, sprite: Sprite, speed: float, target: Vector | None = None
    ) -> None:
        self._target: Vector | None = target
        self._sprite: Sprite = sprite
        self._speed: float = speed

    @property
    def target(self) -> Vector | None:
        return self._target

    def move(self) -> None:
        if self.target is None:
            return

        movement: Vector = self.target - self._sprite.xy
        if movement.length() < self._speed:
            self._sprite.xy += movement
            return

        self._sprite.xy += movement.normalise() * self._speed

    def rotate(self) -> None:
        if self.target is None:
            return

        self._sprite.face_point(self.target.convert())

    def update_target(self, target: Vector | None = None) -> None:
        self._target = target
