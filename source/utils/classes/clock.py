# /utils/classes/clock.py


# Define Clock Class
class Clock:
    """`Clock` class that represent a ticking clock for time tracking"""

    __slots__ = "_time"

    def __init__(self) -> None:
        """Initialise a `Clock` object"""

        # Define private attribute
        self._time: float = 0

    @property
    def time(self) -> float:
        """Get current value of time attribute

        Returns:
            float: The current time value (in milliseconds)
        """

        return self._time

    def update(self, delta_time: float) -> None:
        """Update the clock with a change in time

        Args:
            delta_time (float): The change in time since last tick
        """

        # Update by 'delta_time' in milliseconds
        self._time += delta_time * 1000
