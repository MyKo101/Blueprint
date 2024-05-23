"""This modules contains the basic Generator classes."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar


# region TypeVars used by generics

T = TypeVar("T", bool, str, float, int)
T_SFI = TypeVar("T_SFI", str, float, int)
T_FI = TypeVar("T_FI", float, int)
T_F = TypeVar("T_F", float, float)
T_B = TypeVar("T_B", bool, bool)
# endregion

# region Generic Classes


@dataclass
class Generator(Generic[T], ABC):
    """Basic Abstract Generator Class."""

    @abstractmethod
    def generate(self, n: int) -> list[T]:
        """Generate n values."""
        ...


@dataclass
class GeneratorComposite(Generator[T], ABC):
    """A Composite Generator that combines two Generators."""

    left: Generator[T]
    right: Generator[T]

    @abstractmethod
    def generate(self, n: int) -> list[T]:
        """Generate n values."""
        ...

    def zip_generators(self, n: int) -> zip[tuple[T, T]]:
        """Zip the values generated by the two Generators."""
        lhs_values: list[T] = self.left.generate(n)
        rhs_values: list[T] = self.right.generate(n)

        return zip(lhs_values, rhs_values, strict=True)


# endregion

# region Abstract Typed Base Classes


@dataclass
class GeneratorBool(Generator[bool], ABC):
    """Abstract Base Class for Generators that generate booleans."""


@dataclass
class GeneratorStr(Generator[str], ABC):
    """Abstract Base Class for Generators that generate strings."""


@dataclass
class GeneratorFloat(Generator[float], ABC):
    """Abstract Base Class for Generators that generate floats."""


@dataclass
class GeneratorInt(Generator[int], ABC):
    """Abstract Base Class for Generators that generate integers."""


# endregion

# region Abstract Typed Composite Classes


@dataclass
class GeneratorCompositeAdd(GeneratorComposite[T_SFI], ABC):
    """A Composite Generator that adds two Generators."""

    def generate(self, n: int) -> list[T_SFI]:
        """Generate n values by adding the two generated values."""
        return [a + b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeSub(GeneratorComposite[T_FI], ABC):
    """A Composite Generator that subtracts two Generators."""

    def generate(self, n: int) -> list[T_FI]:
        """Generate n values by subtracting the two generated values."""
        return [a - b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeMult(GeneratorComposite[T_FI], ABC):
    """A Composite Generator that multiplies two Generators."""

    def generate(self, n: int) -> list[T_FI]:
        """Generate n values by multiplying the two generated values."""
        return [a * b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeTrueDiv(GeneratorComposite[T_F], ABC):
    """A Composite Generator that divides two Generators."""

    def generate(self, n: int) -> list[T_F]:
        """Generate n values by dividing the two generated values."""
        return [a / b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeFloorDiv(GeneratorComposite[T_FI], ABC):
    """A Composite Generator that floor divides two Generators."""

    def generate(self, n: int) -> list[T_FI]:
        """Generate n values by floor dividing the two generated values."""
        return [a // b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositePow(GeneratorComposite[T_FI], ABC):
    """A Composite Generator that exponentiates two Generators."""

    def generate(self, n: int) -> list[T_FI]:
        """Generate n values by exponentiating the two generated values."""
        return [a**b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeAnd(GeneratorComposite[T_B], ABC):
    """A Composite Generator that ands two Generators."""

    def generate(self, n: int) -> list[T_B]:
        """Generate n values by anding the two generated values."""
        return [a and b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeOr(GeneratorComposite[T_B], ABC):
    """A Composite Generator that ors two Generators."""

    def generate(self, n: int) -> list[T_B]:
        """Generate n values by oring the two generated values."""
        return [a or b for a, b in self.zip_generators(n)]


@dataclass
class GeneratorCompositeXor(GeneratorComposite[T_B], ABC):
    """A Composite Generator that xors two Generators."""

    def generate(self, n: int) -> list[T_B]:
        """Generate n values by xoring the two generated values."""
        return [a ^ b for a, b in self.zip_generators(n)]


# endregion

# region Composite Classes

# region Compite Classes for Addition


@dataclass
class GeneratorCompositeAddStr(GeneratorCompositeAdd[str], GeneratorStr):
    """A Composite Generator that adds two String Generators."""


@dataclass
class GeneratorCompositeAddFloat(GeneratorCompositeAdd[float], GeneratorFloat):
    """A Composite Generator that adds two Float Generators."""


@dataclass
class GeneratorCompositeAddInt(GeneratorCompositeAdd[int], GeneratorInt):
    """A Composite Generator that adds two Integer Generators."""


# endregion
# region Compite Classes for Subtraction


@dataclass
class GeneratorCompositeSubFloat(GeneratorCompositeSub[float], GeneratorFloat):
    """A Composite Generator that subtracts two Float Generators."""


@dataclass
class GeneratorCompositeSubInt(GeneratorCompositeSub[int], GeneratorInt):
    """A Composite Generator that subtracts two Integer Generators."""


# endregion

# region Composite Classes for Multiplication


@dataclass
class GeneratorCompositeMultFloat(GeneratorCompositeMult[float], GeneratorFloat):
    """A Composite Generator that multiplies two Float Generators."""


@dataclass
class GeneratorCompositeMultInt(GeneratorCompositeMult[int], GeneratorInt):
    """A Composite Generator that multiplies two Integer Generators."""


# endregion
# region Composite Classes for True Division


@dataclass
class GeneratorCompositeTrueDivFloat(GeneratorCompositeTrueDiv[float], GeneratorFloat):
    """A Composite Generator that divides two Float Generators."""


# endregion
# region Composite Classes for Floor Division


@dataclass
class GeneratorCompositeFloorDivFloat(
    GeneratorCompositeFloorDiv[float], GeneratorFloat
):
    """A Composite Generator that floor divides two Float Generators."""


@dataclass
class GeneratorCompositeFloorDivInt(GeneratorCompositeFloorDiv[int], GeneratorInt):
    """A Composite Generator that floor divides two Integer Generators."""


# endregion
# region Composite Classes for Power


@dataclass
class GeneratorCompositePowFloat(GeneratorCompositePow[float], GeneratorFloat):
    """A Composite Generator that exponentiates two Float Generators."""


@dataclass
class GeneratorCompositePowInt(GeneratorCompositePow[int], GeneratorInt):
    """A Composite Generator that exponentiates two Integer Generators."""


# endregion
# region Composite Classes for And


@dataclass
class GeneratorCompositeAndBool(GeneratorCompositeAnd[bool], GeneratorBool):
    """A Composite Generator that ands two Boolean Generators."""


# endregion
# region Composite Classes for Or


@dataclass
class GeneratorCompositeOrBool(GeneratorCompositeOr[bool], GeneratorBool):
    """A Composite Generator that ors two Boolean Generators."""


# endregion

# region Composite Classes for Xor


@dataclass
class GeneratorCompositeXorBool(GeneratorCompositeXor[bool], GeneratorBool):
    """A Composite Generator that xors two Boolean Generators."""


# endregion


# endregion
