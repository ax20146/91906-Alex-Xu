from ..utils import ClassSpriteList, Sprite, Timer, TuplePoint


class Particle(Sprite):
    lst: ClassSpriteList

    def __init__(
        self,
        filename: str,
        *,
        rotation: float = 0,
        position: TuplePoint = (0, 0),
        delay: int = 0,
    ) -> None:
        super().__init__(
            filename,
            rotation=rotation,
            position=position,
        )

        self.lst.append(self)
        self.timer: Timer = Timer(delay, self.clock)

    def on_update(self, dt: float) -> None:
        if self.timer.available():
            self.kill()
