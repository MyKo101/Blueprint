"""RandomInt field generator."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .generators import GeneratorInt


# class RandomInt(FieldGenerator[int]):

#     def generate(self, n: int) -> list[int]:
#         return [random.randint(0, 100) for _ in range(n)]


def generate_int(low: int, high: int) -> int:
    """Generate a random integer between low and high.

    Args:
        low: The lower bound of the random integer.
        high: The upper bound of the random integer.

    Returns:
        int: A random integer between low and high.
    """
    return random.randint(low, high)  # noqa: S311


@dataclass
class RandomInt(GeneratorInt):
    """A Generator that generates random integers."""

    low: int
    high: int

    def generate(self, n: int) -> list[int]:
        """Generate n random integers between low and high."""
        return [generate_int(self.low, self.high) for _ in range(n)]

    def copy(self) -> RandomInt:
        """Return a copy of the RandomInt object."""
        return RandomInt(self.low, self.high)
