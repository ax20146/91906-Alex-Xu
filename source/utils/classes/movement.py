# /utils/classes/movement.py


from .sprite import Sprite
from .vector import Vector


class Movement:
    __slots__ = "_target", "_speed", "_sprite"

    def __init__(
        self, sprite: Sprite, target: Vector, speed: float = 0
    ) -> None:
        self._sprite: Sprite = sprite
        self._target: Vector = target
        self._speed: float = speed

    @property
    def target(self) -> Vector:
        return self._target

    def move(self) -> None:
        movement: Vector = self.target - self._sprite.xy
        if movement.length() < self._speed:
            self._sprite.xy += movement
            return

        self._sprite.xy += movement.normalise() * self._speed

    def rotate(self) -> None:
        self._sprite.face_point(self.target.convert())

    def update_target(self, target: Vector) -> None:
        self._target = target
