"""This modules contains the basic Generator classes."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field

# from typing import Self
from typing import Generic
from typing import TypeVar
from typing import Union

from typing_extensions import Self

from .zipper_function import zipper


# region TypeVars used by generics

T = TypeVar("T", bool, str, float, int)
U = TypeVar("U", bool, str, float, int)
T_SFI = TypeVar("T_SFI", str, float, int)
T_BFI = TypeVar("T_BFI", bool, float, int)
T_FI = TypeVar("T_FI", float, int)
T_BI = TypeVar("T_BI", bool, int)
T_BF = TypeVar("T_BF", bool, float)
T_F = TypeVar("T_F", float, float)
T_B = TypeVar("T_B", bool, bool)
T_I = TypeVar("T_I", int, int)

Numeric = Union[int, float]

# endregion

# region Generic Abstract Classes


@dataclass
class Generator(Generic[T], ABC):
    """Basic Abstract Generator Class."""

    cache: list[T] = field(default_factory=list, init=False, repr=False)

    @abstractmethod
    def generate(self, n: int) -> list[T]:
        """Generate n values.

        Args:
            n (int): The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        ...

    def generate_cache(self, n: int) -> list[T]:
        """Generate n cached values.

        Args:
            n (int):The number of values to generate or recall.

        Returns:
            list[T]: The generated values.
        """
        if len(self.cache) < n:
            self.cache.extend(self.generate(n - len(self.cache)))
        return self.cache[:n]

    @abstractmethod
    def copy(self) -> Self:
        """Create a copy of the Generator.

        Returns:
            Self: The copied Generator.
        """
        ...

    def to_int(self) -> GeneratorInt:
        """Convert the Generator to a Generator of integers.

        Returns:
            GeneratorInt: The converted Generator.
        """
        return GeneratorWrapperInt(self)

    def to_float(self) -> GeneratorFloat:
        """Convert the Generator to a Generator of floats.

        Returns:
            GeneratorFloat: The converted Generator.
        """
        return GeneratorWrapperFloat(self)

    def to_str(self) -> GeneratorStr:
        """Convert the Generator to a Generator of strings.

        Returns:
            GeneratorStr: The converted Generator.
        """
        return GeneratorWrapperStr(self)

    def to_bool(self) -> GeneratorBool:
        """Convert the Generator to a Generator of booleans.

        Returns:
            GeneratorBool: The converted Generator.
        """
        return GeneratorWrapperBool(self)


@dataclass
class GeneratorComposite(Generator[T], ABC):
    """A Composite Generator that combines two Generators.

    Args:
        left (Generator[T]): The left Generator.
        right (Generator[T]): The right Generator.
    """

    left: Generator[T]
    right: Generator[T]

    @abstractmethod
    def op(self, a: T, b: T) -> T:
        """Perform the operation on the two values.

        Args:
            a (T): The first value.
            b (T): The second value.

        Returns:
            T: The result of the operation.
        """
        ...

    def generate(self, n: int) -> list[T]:
        """Generate n values by combining the two generated values.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T_SFI]: The generated values.
        """
        return [self.op(a, b) for a, b in self.zip_generators(n)]

    def generate_cache(self, n: int) -> list[T]:
        """Generate n values by combining the two generated values.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [self.op(a, b) for a, b in self.zip_generators(n, from_cache=True)]

    def zip_generators(self, n: int, *, from_cache: bool = False) -> zip[tuple[T, ...]]:
        """Zip the two generators together for iteration.

        Args:
            n (int): The number of values to generate.
            from_cache (bool): Whether to generate from cache.

        Returns:
            zip[tuple[T, ...]]: The zipped values.
        """
        lhs_values: list[T]
        rhs_values: list[T]
        if from_cache:
            lhs_values = self.left.generate_cache(n)
            rhs_values = self.right.generate_cache(n)
        else:
            lhs_values = self.left.generate(n)
            rhs_values = self.right.generate(n)
        return zipper(lhs_values, rhs_values)

    def copy(self) -> Self:
        """Create a copy of the GeneratorComposite.

        Returns:
            Self: The copied GeneratorComposite.
        """
        return self.__class__(self.left.copy(), self.right.copy())


@dataclass
class GeneratorWrapper(Generator[T], Generic[U, T], ABC):
    """A Wrapper class for converting Generators.

    Args:
        internal (Generator[U]): The internal Generator.
    """

    internal: Generator[U]

    @abstractmethod
    def wrap_type(self) -> type[T]:
        """Wrap the internal value to the response type.

        Returns:
            type[T]: The wrapped value.
        """
        ...

    def copy(self) -> Self:
        """Create a copy of the GeneratorWrapper.

        Returns:
            Self: The copied GeneratorWrapper.
        """
        return self.__class__(self.internal.copy())

    @staticmethod
    def convert(x: U, t: type[T]) -> T:
        """Convert the internal value to the response type.

        Args:
            x (U): The value to convert.
            t (type[T]): The type to convert to.

        Returns:
            T: The converted value.
        """
        try:
            return t(x)
        except ValueError:
            return t()

    def generate(self, n: int) -> list[T]:
        """Generate n values by converting the generated values to floats.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [
            GeneratorWrapper.convert(x, self.wrap_type())
            for x in self.internal.generate(n)
        ]

    def generate_cache(self, n: int) -> list[T]:
        """Generate n values by converting the generated values to floats.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [
            GeneratorWrapper.convert(x, self.wrap_type())
            for x in self.internal.generate_cache(n)
        ]


@dataclass
class GeneratorConstant(Generator[T]):
    """A Generator that generates a constant value.

    Args:
        value (T): The constant value to generate.
    """

    value: T

    def generate_cache(self, n: int) -> list[T]:
        """Generate n cached values.

        Args:
            n (int): The number of values to generate or recall.

        Returns:
            list[T]: The generated values.
        """
        return self.generate(n)

    def generate(self, n: int) -> list[T]:
        """Generate n values.

        Args:
            n (int): The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [self.value for _ in range(n)]

    def copy(self) -> Self:
        """Create a copy of the Generator.

        Returns:
            Self: The copied Generator.
        """
        return self.__class__(self.value)


# endregion

# region Abstract Typed Base Classes


@dataclass
class GeneratorBool(Generator[bool], ABC):
    """Abstract Base Class for Generators that generate booleans."""

    def to_bool(self) -> GeneratorBool:
        """Convert the Generator to a Generator of booleans.

        Returns:
            GeneratorBool: The converted Generator.
        """
        return self

    @staticmethod
    def coerce(x: GeneratorBool | bool) -> GeneratorBool:
        """Coerce a boolean to a GeneratorBool.

        Args:
            x (GeneratorBool|bool): The value to coerce.

        Returns:
            GeneratorBool: The coerced value.
        """
        if isinstance(x, bool):
            return GeneratorConstantBool(x)
        return x

    def __and__(self, other: GeneratorBool | bool) -> GeneratorCompositeAndBool:
        """Perform 'And' on boolean Generators (or constant).

        Args:
            other (GeneratorBool | bool): The other boolean Generator.

        Returns:
            GeneratorCompositeAndBool: The Composite Generator.
        """
        other = GeneratorBool.coerce(other)
        return GeneratorCompositeAndBool(self, other)

    def __or__(self, other: GeneratorBool | bool) -> GeneratorCompositeOrBool:
        """Perform 'Or' on boolean Generators (or constant).

        Args:
            other (GeneratorBool | bool): The other boolean Generator.

        Returns:
            GeneratorCompositeOrBool: The Composite Generator.
        """
        other = GeneratorBool.coerce(other)
        return GeneratorCompositeOrBool(self, other)

    def __xor__(self, other: GeneratorBool | bool) -> GeneratorCompositeXorBool:
        """Perform 'Xor' on boolean Generators (or constant).

        Args:
            other (GeneratorBool | bool): The other boolean Generator.

        Returns:
            GeneratorCompositeXorBool: The Composite Generator.
        """
        other = GeneratorBool.coerce(other)
        return GeneratorCompositeXorBool(self, other)


@dataclass
class GeneratorStr(Generator[str], ABC):
    """Abstract Base Class for Generators that generate strings."""

    def to_str(self) -> GeneratorStr:
        """Convert the Generator to a Generator of strings.

        Returns:
            GeneratorStr: The converted Generator.
        """
        return self

    @staticmethod
    def coerce(x: GeneratorStr | str) -> GeneratorStr:
        """Coerce a string to a GeneratorStr.

        Args:
            x (GeneratorStr|str): The value to coerce.

        Returns:
            GeneratorStr: The coerced value.
        """
        if isinstance(x, str):
            return GeneratorConstantStr(x)
        return x

    def __add__(self, other: GeneratorStr) -> GeneratorCompositeAddStr:
        """Perform 'Add' on string Generators (or constant).

        Args:
            other (GeneratorStr): The other string Generator.

        Returns:
            GeneratorCompositeAddStr: The Composite Generator.
        """
        other = GeneratorStr.coerce(other)
        return GeneratorCompositeAddStr(self, other)


@dataclass
class GeneratorFloat(Generator[float], ABC):
    """Abstract Base Class for Generators that generate floats."""

    def to_float(self) -> GeneratorFloat:
        """Convert the Generator to a Generator of floats.

        Returns:
            GeneratorFloat: The converted Generator.
        """
        return self

    @staticmethod
    def coerce(x: GeneratorNumeric | Numeric) -> GeneratorFloat:
        """Coerce a numeric to a GeneratorFloat.

        Args:
            x (GeneratorNumeric|Numeric): The value to coerce.

        Returns:
            GeneratorFloat: The coerced value.
        """
        if isinstance(x, int):
            return GeneratorConstantFloat(float(x))
        if isinstance(x, float):
            return GeneratorConstantFloat(x)
        if isinstance(x, GeneratorInt):
            return x.to_float()
        return x

    def __add__(self, other: GeneratorNumeric | Numeric) -> GeneratorCompositeAddFloat:
        """Perform 'Add' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeAddFloat: The Composite Generator.
        """
        other = GeneratorFloat.coerce(other)
        return GeneratorCompositeAddFloat(self, other)

    def __sub__(self, other: GeneratorNumeric | Numeric) -> GeneratorCompositeSubFloat:
        """Perform 'Subtract' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeSubFloat: The Composite Generator.
        """
        other = GeneratorFloat.coerce(other)
        return GeneratorCompositeSubFloat(self, other)

    def __mul__(self, other: GeneratorNumeric | Numeric) -> GeneratorCompositeMultFloat:
        """Perform 'Multiply' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeMultFloat: The Composite Generator.
        """
        other = GeneratorFloat.coerce(other)
        return GeneratorCompositeMultFloat(self, other)

    def __truediv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeTrueDivFloat:
        """Perform 'Divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeTrueDivFloat: The Composite Generator.
        """
        other = GeneratorFloat.coerce(other)
        return GeneratorCompositeTrueDivFloat(self, other)

    def __floordiv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeFloorDivFloat:
        """Perform 'Floor divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeFloorDivFloat: The Composite Generator.
        """
        other = GeneratorFloat.coerce(other)
        return GeneratorCompositeFloorDivFloat(self, other)


@dataclass
class GeneratorInt(Generator[int], ABC):
    """Abstract Base Class for Generators that generate integers."""

    def to_int(self) -> GeneratorInt:
        """Convert the Generator to a Generator of integers.

        Returns:
            GeneratorInt: The converted Generator.
        """
        return self

    @staticmethod
    def coerce(x: GeneratorNumeric | Numeric) -> GeneratorNumeric:
        """Coerce a numeric to a GeneratorFloat.

        Args:
            x (GeneratorNumeric|Numeric): The value to coerce.

        Returns:
            GeneratorNumeric: The coerced value.
        """
        if isinstance(x, int):
            return GeneratorConstantInt(x)
        if isinstance(x, float):
            return GeneratorConstantFloat(x)
        return x

    def __add__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeAddNumeric:
        """Perform 'Add' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeAddNumeric: The Composite Generator.
        """
        other = GeneratorInt.coerce(other)
        if isinstance(other, GeneratorFloat):
            return GeneratorCompositeAddFloat(self.to_float(), other)
        return GeneratorCompositeAddInt(self, other)

    def __sub__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeSubNumeric:
        """Perform 'Subtract' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeSubNumeric: The Composite Generator.
        """
        other = GeneratorInt.coerce(other)
        if isinstance(other, GeneratorFloat):
            return GeneratorCompositeSubFloat(self.to_float(), other)
        return GeneratorCompositeSubInt(self, other)

    def __mul__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeMultNumeric:
        """Perform 'Multiply' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeMultNumeric: The Composite Generator.
        """
        other = GeneratorInt.coerce(other)
        if isinstance(other, GeneratorFloat):
            return GeneratorCompositeMultFloat(self.to_float(), other)
        return GeneratorCompositeMultInt(self, other)

    def __floordiv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeFloorDivNumeric:
        """Perform 'Floor divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeFloorDivNumeric: The Composite Generator.
        """
        other = GeneratorInt.coerce(other)
        if isinstance(other, GeneratorFloat):
            return GeneratorCompositeFloorDivFloat(self.to_float(), other)
        return GeneratorCompositeFloorDivInt(self, other)


# endregion

# region Wrapper Classes


@dataclass
class GeneratorWrapperStr(GeneratorStr, GeneratorWrapper[U, str]):
    """A Wrapper class for converting Generators to string Generators."""

    def wrap_type(self) -> type[str]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[str]: The wrapped value.
        """
        return str


@dataclass
class GeneratorWrapperFloat(GeneratorFloat, GeneratorWrapper[U, float]):
    """A Wrapper class for converting Generators to float Generators."""

    def wrap_type(self) -> type[float]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[float]: The wrapped value.
        """
        return float


@dataclass
class GeneratorWrapperInt(GeneratorInt, GeneratorWrapper[U, int]):
    """A Wrapper class for converting Generators to integer Generators."""

    def wrap_type(self) -> type[int]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[int]: The wrapped value.
        """
        return int


@dataclass
class GeneratorWrapperBool(GeneratorBool, GeneratorWrapper[U, bool]):
    """A Wrapper class for converting Generators to boolean Generators."""

    def wrap_type(self) -> type[bool]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[bool]: The wrapped value.
        """
        return bool


# endregion

# region Abstract Typed Composite Classes


@dataclass
class GeneratorCompositeAdd(GeneratorComposite[T_SFI]):
    """A Composite Generator that adds two Generators."""

    def op(self, a: T_SFI, b: T_SFI) -> T_SFI:
        """Perform addition on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            T_SFI: The result of the operation.
        """
        return a + b


@dataclass
class GeneratorCompositeSub(GeneratorComposite[T_FI]):
    """A Composite Generator that subtracts two Generators."""

    def op(self, a: T_FI, b: T_FI) -> T_FI:
        """Perform subtraction on two values.

        Args:
            a (T_FI): The first value.
            b (T_FI): The second value.

        Returns:
            T_FI: The result of the operation.
        """
        return a - b


@dataclass
class GeneratorCompositeMult(GeneratorComposite[T_FI]):
    """A Composite Generator that multiplies two Generators."""

    def op(self, a: T_FI, b: T_FI) -> T_FI:
        """Perform multiplication on two values.

        Args:
            a (T_FI): The first value.
            b (T_FI): The second value.

        Returns:
            T_FI: The result of the operation.
        """
        return a * b


@dataclass
class GeneratorCompositeTrueDiv(GeneratorComposite[T_F]):
    """A Composite Generator that divides two Generators."""

    def op(self, a: T_F, b: T_F) -> T_F:
        """Perform true division on two values.

        Args:
            a (T_F): The first value.
            b (T_F): The second value.

        Returns:
            T_F: The result of the operation.
        """
        return a / b


@dataclass
class GeneratorCompositeFloorDiv(GeneratorComposite[T_FI]):
    """A Composite Generator that floor divides two Generators."""

    def op(self, a: T_FI, b: T_FI) -> T_FI:
        """Perform floor division on two values.

        Args:
            a (T_FI): The first value.
            b (T_FI): The second value.

        Returns:
            T_FI: The result of the operation.
        """
        return a // b


@dataclass
class GeneratorCompositeAnd(GeneratorComposite[T_B]):
    """A Composite Generator that ands two Generators."""

    def op(self, a: T_B, b: T_B) -> T_B:
        """Perform and on two values.

        Args:
            a (T_B): The first value.
            b (T_B): The second value.

        Returns:
            T_B: The result of the operation.
        """
        return a and b


@dataclass
class GeneratorCompositeOr(GeneratorComposite[T_B]):
    """A Composite Generator that ors two Generators."""

    def op(self, a: T_B, b: T_B) -> T_B:
        """Perform or on two values.

        Args:
            a (T_B): The first value.
            b (T_B): The second value.

        Returns:
            T_B: The result of the operation.
        """
        return a or b


@dataclass
class GeneratorCompositeXor(GeneratorComposite[T_B]):
    """A Composite Generator that xors two Generators."""

    def op(self, a: T_B, b: T_B) -> T_B:
        """Perform xor on two values.

        Args:
            a (T_B): The first value.
            b (T_B): The second value.

        Returns:
            T_B: The result of the operation.
        """
        return a ^ b


# endregion

# region Composite Classes

# region Composite Classes for Addition


@dataclass
class GeneratorCompositeAddStr(GeneratorStr, GeneratorCompositeAdd[str]):
    """A Composite Generator that adds two String Generators."""


@dataclass
class GeneratorCompositeAddFloat(GeneratorFloat, GeneratorCompositeAdd[float]):
    """A Composite Generator that adds two Float Generators."""


@dataclass
class GeneratorCompositeAddInt(GeneratorInt, GeneratorCompositeAdd[int]):
    """A Composite Generator that adds two Integer Generators."""


# endregion
# region Composite Classes for Subtraction


@dataclass
class GeneratorCompositeSubFloat(GeneratorFloat, GeneratorCompositeSub[float]):
    """A Composite Generator that subtracts two Float Generators."""


@dataclass
class GeneratorCompositeSubInt(GeneratorInt, GeneratorCompositeSub[int]):
    """A Composite Generator that subtracts two Integer Generators."""


# endregion
# region Composite Classes for Multiplication


@dataclass
class GeneratorCompositeMultFloat(GeneratorFloat, GeneratorCompositeMult[float]):
    """A Composite Generator that multiplies two Float Generators."""


@dataclass
class GeneratorCompositeMultInt(GeneratorInt, GeneratorCompositeMult[int]):
    """A Composite Generator that multiplies two Integer Generators."""


# endregion
# region Composite Classes for True Division


@dataclass
class GeneratorCompositeTrueDivFloat(GeneratorFloat, GeneratorCompositeTrueDiv[float]):
    """A Composite Generator that divides two Float Generators."""


# endregion
# region Composite Classes for Floor Division


@dataclass
class GeneratorCompositeFloorDivFloat(
    GeneratorCompositeFloorDiv[float], GeneratorFloat
):
    """A Composite Generator that floor divides two Float Generators."""


@dataclass
class GeneratorCompositeFloorDivInt(GeneratorInt, GeneratorCompositeFloorDiv[int]):
    """A Composite Generator that floor divides two Integer Generators."""


# endregion
# region Composite Classes for And


@dataclass
class GeneratorCompositeAndBool(GeneratorBool, GeneratorCompositeAnd[bool]):
    """A Composite Generator that ands two Boolean Generators."""


# endregion
# region Composite Classes for Or


@dataclass
class GeneratorCompositeOrBool(GeneratorBool, GeneratorCompositeOr[bool]):
    """A Composite Generator that ors two Boolean Generators."""


# endregion
# region Composite Classes for Xor


@dataclass
class GeneratorCompositeXorBool(GeneratorBool, GeneratorCompositeXor[bool]):
    """A Composite Generator that xors two Boolean Generators."""


# endregion


# region Constant Generators


@dataclass
class GeneratorConstantStr(GeneratorStr, GeneratorConstant[str]):
    """A Generator that generates a constant string value."""


@dataclass
class GeneratorConstantBool(GeneratorBool, GeneratorConstant[bool]):
    """A Generator that generates a constant boolean value."""


@dataclass
class GeneratorConstantInt(GeneratorInt, GeneratorConstant[int]):
    """A Generator that generates a constant integer value."""


@dataclass
class GeneratorConstantFloat(GeneratorFloat, GeneratorConstant[float]):
    """A Generator that generates a constant float value."""


# endregion


# region Types
GeneratorCompositeAddNumeric = Union[
    GeneratorCompositeAddInt, GeneratorCompositeAddFloat
]
GeneratorCompositeSubNumeric = Union[
    GeneratorCompositeSubInt, GeneratorCompositeSubFloat
]
GeneratorCompositeMultNumeric = Union[
    GeneratorCompositeMultInt, GeneratorCompositeMultFloat
]
GeneratorCompositeTrueDivNumeric = GeneratorCompositeTrueDivFloat
GeneratorCompositeFloorDivNumeric = Union[
    GeneratorCompositeFloorDivInt, GeneratorCompositeFloorDivFloat
]
GeneratorNumeric = Union[GeneratorInt, GeneratorFloat]
GeneratorAny = Union[GeneratorInt, GeneratorFloat, GeneratorStr, GeneratorBool]

# endregion
