# /utils/types.py
"""`Types` module containing utility types."""


# Import Built-in Dependencies
from typing import Any, Callable, ClassVar, Iterator, NamedTuple, TypeVar

# Export Local Types
__all__: list[str] = [
    "Any",
    "ClassVar",
    "Callable",
    "Iterator",
    "NamedTuple",
    "Type",
]


# Define generic type
Type = TypeVar("Type")
