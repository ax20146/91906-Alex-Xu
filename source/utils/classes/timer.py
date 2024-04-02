# /utils/classes/timer.py
"""`Timer` module containing the `Timer` class."""


# Import Local Dependencies
from .clock import Clock


# Define Timer class
class Timer:
    """`Timer` object represents a timer for duration tracking."""

    # Define slots of timer
    # NOTE: Done for memory optimisation
    __slots__ = "disable", "duration", "_clock", "_previous"

    def __init__(
        self, clock: Clock, duration: int = 0, *, initialise: bool = True
    ) -> None:
        """Initialise a `Timer` object.

        Args:
            clock (Clock): The clock for time tracking.
            duration (int, optional): The duration to track.
                Defaults to 0.
            initialise (bool, optional): Whether to time immediately.
                Defaults to True.
        """

        # Define public attributes of clock
        self.disable: bool = False
        self.duration: int = abs(duration)

        # Define protected attributes of clock
        # NOTE: Done in case external code modifies
        # 'clock' instance or 'previous' time
        self._clock: Clock = clock
        self._previous: float = (
            self._clock.time
            if initialise
            else self._clock.time - self.duration
        )

    def available(self) -> bool:
        """Determine whether the timer is available for timing again.

        Returns:
            bool: Whether the timer is available.
        """

        return (
            False
            if self.disable
            else self._clock.time - self._previous >= self.duration
        )

    def update(self) -> None:
        """Update the timer with new time to track duration again."""

        self._previous = self._clock.time
