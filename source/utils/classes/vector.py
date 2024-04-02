# /utils/classes/vector.py
"""`Vector` module containing the `Vector` class."""


# Import Built-in Dependencies
from __future__ import annotations

from dataclasses import dataclass
from math import hypot
from random import randint
from typing import SupportsIndex


# Define Vector dataclass
@dataclass(repr=False, frozen=True, slots=True)
class Vector:
    """`Vector` object represents a mathematical vector."""

    # Define initialisation parameters & vector public attributes
    x: float = 0
    y: float = 0

    def __repr__(self) -> str:
        """Implement the behaviour for built-in
        representation `repr()` function.

        Returns:
            str: The representation string of the vector.
        """

        return f"({self.x}, {self.y})"

    def __add__(self, __value: Vector) -> Vector:
        """Implement the behaviour for built-in
        addition `+` operator.

        Functionality: See 'vector addition & subtraction'.

        Args:
            __value (Vector): The vector operand for addition.

        Returns:
            Vector: The resultant vector.
        """

        return self.__class__(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: Vector) -> Vector:
        """Implement the behaviour for built-in
        subtraction `-` operator.

        Functionality: See 'vector addition & subtraction'.

        Args:
            __value (Vector): The vector operand for subtraction.

        Returns:
            Vector: The resultant vector.
        """

        return self.__class__(self.x - __value.x, self.y - __value.y)

    def __mul__(self, __value: float) -> Vector:
        """Implement the behaviour for built-in
        multiplication `*` operator.

        Functionality: See 'scalar multiplication & division'.

        Args:
            __value (float): The scalar operand for multiplication.

        Returns:
            Vector: The resultant vector.
        """

        return self.__class__(self.x * __value, self.y * __value)

    def __truediv__(self, __value: float) -> Vector:
        """Implement the behaviour for built-in
        division `/` operator.

        Functionality: See 'scalar multiplication & division'.

        Args:
            __value (float): The scalar operand for division.

        Returns:
            Vector: The resultant vector.
        """

        return self.__class__(self.x / __value, self.y / __value)

    def __abs__(self) -> float:
        """Implement the behaviour for built-in
        absolute value `abs()` function.

        Returns:
            float: The magnitude (length) of the vector.
        """

        return hypot(self.x, self.y)

    def __round__(self, __ndigits: SupportsIndex = 0) -> Vector:
        """Implement the behaviour for built-in
        round `round()` function.

        Args:
            __ndigits (SupportsIndex, optional):
            The number of digits to round.
                Defaults to 0.

        Returns:
            Vector: The resultant rounded vector.
        """

        return self.__class__(
            round(self.x, __ndigits), round(self.y, __ndigits)
        )

    def length(self) -> float:
        """Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude (length) of the vector.
        """

        return abs(self)

    def normalise(self) -> Vector:
        """Calculate the unit vector magnitude of the vector
        (Length of 1).

        Returns:
            Vector: The resultant normalised unit vector.
        """

        return self / abs(self)

    def within(self, __value: Vector, /, radius: float) -> bool:
        """Determine whether a vector is within the a certain radius.

        Args:
            __value (Vector): The other vector used in calculation.
            radius (float): The radius round the vector.

        Returns:
            bool: Whether the vector is within the radius of another.
        """

        return abs(self - __value) <= radius

    def limit(self, lower: Vector, upper: Vector) -> Vector:
        """Limit the vector within some lower and upper bound.

        Args:
            lower (Vector): The lower bound vector.
            upper (Vector): The upper bound vector.
        Returns:
            Vector: The resultant vector limited to the bounds.
        """

        return self.__class__(
            min(max(self.x, lower.x), upper.x),
            min(max(self.y, lower.y), upper.y),
        )

    def randomise(self, radius: int) -> Vector:
        """Randomise the vector within some radius range.

        Args:
            radius (int): The radius to randomise within.

        Returns:
            Vector: The resultant vector randomised within the radius.
        """

        return self.__class__(
            randint(round(self.x - radius), round(self.x + radius)),
            randint(round(self.y - radius), round(self.y + radius)),
        )

    def convert(self) -> tuple[float, float]:
        """Convert the vector into a tuple structure.

        Returns:
            tuple[float, float]: The tuple with the vector data.
        """

        return (self.x, self.y)
