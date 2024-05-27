"""Zipper class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import Iterable
from typing import TypeVar


T = TypeVar("T")


@dataclass
class Zipper(Generic[T]):
    """A class to zip two lists together."""

    data: tuple[Iterable[T] | T, ...]
    loc: int = 0
    length: int = 0

    def __init__(self, *args: Iterable[T] | T, length: int | None = None) -> None:
        """Initialize the Zipper object.

        Args:
            args (Iterable[T] | T): The lists to zip together.
            length (int | None): The length of the lists.

        Raises:
            ValueError: If length is less than 1.
            ValueError: If length does not match the length of the provided lists.
            ValueError: If the provided lists are not all the same length.

        """
        arg_lengths = [len(a) for a in args if isinstance(a, list)]
        if length is not None and length < 1:
            raise ValueError("Parameter length must be greater than 0.")
        if length is not None and any(a != length for a in arg_lengths):
            raise ValueError(
                "Parameter length must match the length of provided lists."
            )
        # either length is None, or len(args) == length for all args

        arg_lengths_set = set(arg_lengths)
        if len(arg_lengths_set) > 1:
            raise ValueError("All provided lists must be the same length.")

        # All lists are same length and either length is None or len(args) == length
        arg_length = arg_lengths_set.pop() if len(arg_lengths_set) > 0 else length
        self.length = 1 if arg_length is None else arg_length

        self.data = args

    def __iter__(self) -> Zipper[T]:
        """Return the Zipper object to iterate."""
        self.loc = 0
        return self

    def __next__(self) -> tuple[T, ...]:
        """Return the next tuple of values.

        Raises:
            StopIteration: If the Zipper object has been exhausted.

        Returns:
            tuple[T, ...]: The next tuple of values.
        """
        if self.loc >= self.length:
            raise StopIteration
        out = tuple(d[self.loc] if isinstance(d, list) else d for d in self.data)
        self.loc += 1
        return out