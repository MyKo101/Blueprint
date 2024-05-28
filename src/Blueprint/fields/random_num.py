"""RandomInt field generator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from ..generators import GeneratorBool
from ..generators import GeneratorFloat
from ..generators import GeneratorInt
from ..generators import ReferenceFloat
from ..generators import ReferenceInt
from ..generators import zipper
from .random_values import random_bool
from .random_values import random_float
from .random_values import random_int
from .resolve import resolve


T = TypeVar("T", int, float, bool, str)


@dataclass
class RandomInt(GeneratorInt):
    """A Generator that generates random integers."""

    low: ReferenceInt
    high: ReferenceInt

    def generate(self, n: int) -> list[int]:
        """Generate n random integers between low and high."""
        low_z = resolve(self.low, n)
        high_z = resolve(self.high, n)
        return [random_int(low, high) for low, high in zipper(low_z, high_z, length=n)]

    def copy(self) -> RandomInt:
        """Return a copy of the RandomInt object."""
        return RandomInt(self.low, self.high)


@dataclass
class RandomFloat(GeneratorFloat):
    """A Generator that generates random floats."""

    low: ReferenceFloat
    high: ReferenceFloat

    def generate(self, n: int) -> list[float]:
        """Generate n random integers between low and high."""
        low_z = resolve(self.low, n)
        high_z = resolve(self.high, n)
        return [
            random_float(low, high) for low, high in zipper(low_z, high_z, length=n)
        ]

    def copy(self) -> RandomFloat:
        """Return a copy of the RandomFloat object."""
        return RandomFloat(self.low, self.high)


@dataclass
class RandomBool(GeneratorBool):
    """A Generator that generates random booleans."""

    probability: ReferenceFloat

    def generate(self, n: int) -> list[bool]:
        """Generate n random integers between low and high."""
        probability = resolve(self.probability, n)
        return [random_bool(prob) for prob, in zipper(probability, length=n)]

    def copy(self) -> RandomBool:
        """Return a copy of the RandomBool object."""
        return RandomBool(self.probability)
