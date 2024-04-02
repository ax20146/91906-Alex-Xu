# /utils/classes/clock.py
"""`Clock` module containing the `Clock` class."""


# Define Clock class
class Clock:
    """`Clock` object represents a clock for time tracking."""

    # Define slots of clock
    # NOTE: Done for memory optimisation
    __slots__ = "_time"

    def __init__(self) -> None:
        """Initialise a `Clock` object."""

        # Define protected attributes of clock
        # NOTE: Done in case external code modifies 'time'
        self._time: float = 0

    @property
    def time(self) -> float:
        """Get the current clock time value (in milliseconds).

        Returns:
            float: The clock time value.
        """

        return self._time

    def update(self, delta_time: float) -> None:
        """Update the clock time with change in time (in seconds).

        Args:
            delta_time (float): The time difference.
        """

        # Update time with conversion of seconds to milliseconds
        self._time += delta_time * 1000
