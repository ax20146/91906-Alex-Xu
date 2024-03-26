# /utils/classes/timer.py


# Import Local Dependencies
from .clock import Clock


# Define Timer Class
class Timer:
    """`Timer` class that represent a duration timer for cooldown"""

    __slots__ = "delay", "_clock", "_previous"

    def __init__(self, clock: Clock, delay: int) -> None:
        """Initialise a `timer` object

        Args:
            clock (Clock): The clock used for time tracking
            delay (int): The duration to time (0 to disable timing)
        """

        # Define public attributes
        self.delay: int = delay

        # Define private attributes
        self._clock: Clock = clock
        self._previous: float = clock.time

    def available(self) -> bool:
        """Get whether the duration being timed is over

        Returns:
            bool: The result of whether duration is over
        """

        return (
            self._clock.time - self._previous >= self.delay
            if self.delay > 0
            else False
        )

    def update(self) -> None:
        """Update the timer to start re-timing"""

        self._previous = self._clock.time
