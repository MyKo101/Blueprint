"""This modules contains the basic Generator classes."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field

# from typing import Self
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar
from typing import Union

from typing_extensions import Self

from .zipper_function import zipper


# Note on type ignores:
#  For the comparison operators, some type ignore comments are required for
#    for two reasons:
#  1. for the __eq__() and __ne__() operators:
#     The return type of the comparison operators is not a boolean, and so
#          this violates the Liskov substitution principle. However, the
#          implementation of these classes allow for this behavior.
#  2. for the __gt__() and __ge__() operators:
#     The signatures of the operators have unsafe overlap with the __lt__()
#          and __le__() operators. However, the underlying python handles
#          this as expected.

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

if TYPE_CHECKING:
    zt = Union[zip[tuple[T, ...]], zip[tuple[T, ...]]]
else:
    zt = zip


# endregion

# region Generic Abstract Classes


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
class GeneratorOperator(Generator[T], Generic[U, T], ABC):
    """A Operator Generator that performs an operation on two Generators.

    Args:
        left (Generator[U]): The left Generator.
        right (Generator[U]): The right Generator.
    """

    left: Generator[U]
    right: Generator[U]

    @abstractmethod
    def op(self, a: U, b: U) -> T:
        """Perform the operation on the two values.

        Args:
            a (U): The first value.
            b (U): The second value.

        Returns:
            T: The result of the operation.
        """
        ...

    def generate(self, n: int) -> list[T]:
        """Generate n values by operating on the two generated values.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [self.op(a, b) for a, b in self.zip_generators(n)]

    def generate_cache(self, n: int) -> list[T]:
        """Generate n values from cache by operating on the two generated values.

        Args:
            n (int):The number of values to generate.

        Returns:
            list[T]: The generated values.
        """
        return [self.op(a, b) for a, b in self.zip_generators(n, from_cache=True)]

    def zip_generators(self, n: int, *, from_cache: bool = False) -> zt[U]:
        """Zip the two generators together for iteration.

        Args:
            n (int): The number of values to generate.
            from_cache (bool): Whether to generate from cache.

        Returns:
            zt[U]: The zipped values.
        """
        lhs_values: list[U]
        rhs_values: list[U]
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


@dataclass(eq=False, order=False)
class GeneratorComposite(GeneratorOperator[T, T], ABC):
    """A Composite Generator that combines two Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparison(GeneratorOperator[U, bool], ABC):
    """A Comparison Generator that compares two Generators."""


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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
        other_coerced = GeneratorBool.coerce(other)
        return GeneratorCompositeAndBool(self, other_coerced)

    def __or__(self, other: GeneratorBool | bool) -> GeneratorCompositeOrBool:
        """Perform 'Or' on boolean Generators (or constant).

        Args:
            other (GeneratorBool | bool): The other boolean Generator.

        Returns:
            GeneratorCompositeOrBool: The Composite Generator.
        """
        other_coerced = GeneratorBool.coerce(other)
        return GeneratorCompositeOrBool(self, other_coerced)

    def __xor__(self, other: GeneratorBool | bool) -> GeneratorCompositeXorBool:
        """Perform 'Xor' on boolean Generators (or constant).

        Args:
            other (GeneratorBool | bool): The other boolean Generator.

        Returns:
            GeneratorCompositeXorBool: The Composite Generator.
        """
        other_coerced = GeneratorBool.coerce(other)
        return GeneratorCompositeXorBool(self, other_coerced)


@dataclass(eq=False, order=False)
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

    def __add__(self, other: GeneratorStr | str) -> GeneratorCompositeAddStr:
        """Perform 'Add' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorCompositeAddStr: The Composite Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorCompositeAddStr(self, other_coerced)

    def __lt__(  # type: ignore[misc]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonLTStr:
        """Perform 'Less than' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonLTStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonLTStr(self, other_coerced)

    def __le__(  # type: ignore[misc]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonLEStr:
        """Perform 'Less than or equal to' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonLEStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonLEStr(self, other_coerced)

    def __gt__(  # type: ignore[misc]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonGTStr:
        """Perform 'Greater than' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonGTStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonGTStr(self, other_coerced)

    def __ge__(  # type: ignore[misc]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonGEStr:
        """Perform 'Greater than or equal to' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonGEStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonGEStr(self, other_coerced)

    def __eq__(  # type: ignore[override]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonEQStr:
        """Perform 'equality' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonEQStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonEQStr(self, other_coerced)

    def __ne__(  # type: ignore[override]
        self, other: GeneratorStr | str
    ) -> GeneratorComparisonNEStr:
        """Perform 'inequality' on string Generators (or constant).

        Args:
            other (GeneratorStr | str): The other string Generator.

        Returns:
            GeneratorComparisonNEStr: The Comparison Generator.
        """
        other_coerced = GeneratorStr.coerce(other)
        return GeneratorComparisonNEStr(self, other_coerced)


@dataclass(eq=False, order=False)
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
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorCompositeAddFloat(self, other_coerced)

    def __sub__(self, other: GeneratorNumeric | Numeric) -> GeneratorCompositeSubFloat:
        """Perform 'Subtract' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeSubFloat: The Composite Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorCompositeSubFloat(self, other_coerced)

    def __mul__(self, other: GeneratorNumeric | Numeric) -> GeneratorCompositeMultFloat:
        """Perform 'Multiply' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeMultFloat: The Composite Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorCompositeMultFloat(self, other_coerced)

    def __truediv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeTrueDivFloat:
        """Perform 'Divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeTrueDivFloat: The Composite Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorCompositeTrueDivFloat(self, other_coerced)

    def __floordiv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeFloorDivFloat:
        """Perform 'Floor divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeFloorDivFloat: The Composite Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorCompositeFloorDivFloat(self, other_coerced)

    def __lt__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonLTFloat:
        """Perform 'Less than' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonLTFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonLTFloat(self, other_coerced)

    def __le__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonLEFloat:
        """Perform 'Less than or equal to' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonLEFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonLEFloat(self, other_coerced)

    def __gt__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonGTFloat:
        """Perform 'Greater than' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonGTFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonGTFloat(self, other_coerced)

    def __ge__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonGEFloat:
        """Perform 'Greater than or equal to' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonGEFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonGEFloat(self, other_coerced)

    def __eq__(  # type: ignore[override]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonEQFloat:
        """Perform 'equality' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonEQFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonEQFloat(self, other_coerced)

    def __ne__(  # type: ignore[override]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonNEFloat:
        """Perform 'inequality' on float Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other float Generator.

        Returns:
            GeneratorComparisonNEFloat: The Comparison Generator.
        """
        other_coerced = GeneratorFloat.coerce(other)
        return GeneratorComparisonNEFloat(self, other_coerced)


@dataclass(eq=False, order=False)
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
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorCompositeAddFloat(self.to_float(), other_coerced)
        return GeneratorCompositeAddInt(self, other_coerced)

    def __sub__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeSubNumeric:
        """Perform 'Subtract' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeSubNumeric: The Composite Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorCompositeSubFloat(self.to_float(), other_coerced)
        return GeneratorCompositeSubInt(self, other_coerced)

    def __mul__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeMultNumeric:
        """Perform 'Multiply' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeMultNumeric: The Composite Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorCompositeMultFloat(self.to_float(), other_coerced)
        return GeneratorCompositeMultInt(self, other_coerced)

    def __floordiv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeFloorDivNumeric:
        """Perform 'Floor divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeFloorDivNumeric: The Composite Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorCompositeFloorDivFloat(self.to_float(), other_coerced)
        return GeneratorCompositeFloorDivInt(self, other_coerced)

    def __truediv__(
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorCompositeTrueDivFloat:
        """Perform 'True divide' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorCompositeTrueDivFloat: The Composite Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorCompositeTrueDivFloat(self.to_float(), other_coerced)
        return GeneratorCompositeTrueDivFloat(self.to_float(), other_coerced.to_float())

    def __lt__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonLTNumeric:
        """Perform 'Less than' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonLTNumeric: The Comparison Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonLTFloat(self.to_float(), other_coerced)
        return GeneratorComparisonLTInt(self, other_coerced)

    def __le__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonLENumeric:
        """Perform 'Less than or equal to' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonLENumeric: The Comparison Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonLEFloat(self.to_float(), other_coerced)
        return GeneratorComparisonLEInt(self, other_coerced)

    def __gt__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonGTNumeric:
        """Perform 'Greater than' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonGTNumeric: The Comparison Generator.
        """
        # return GeneratorComparisonGTInt(self,GeneratorConstantInt(other))
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonGTFloat(self.to_float(), other_coerced)
        return GeneratorComparisonGTInt(self, other_coerced)

    def __ge__(  # type: ignore[misc]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonGENumeric:
        """Perform 'Greater than or equal to' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonGENumeric: The Comparison Generator.
        """
        # return GeneratorComparisonGTInt(self,GeneratorConstantInt(other))
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonGEFloat(self.to_float(), other_coerced)
        return GeneratorComparisonGEInt(self, other_coerced)

    def __eq__(  # type: ignore[override]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonEQNumeric:
        """Perform 'equality' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonEQNumeric: The Comparison Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonEQFloat(self.to_float(), other_coerced)
        return GeneratorComparisonEQInt(self, other_coerced)

    def __ne__(  # type: ignore[override]
        self, other: GeneratorNumeric | Numeric
    ) -> GeneratorComparisonNENumeric:
        """Perform 'inequality' on numeric Generators (or constant).

        Args:
            other (GeneratorNumeric | Numeric): The other numeric Generator.

        Returns:
            GeneratorComparisonNENumeric: The Comparison Generator.
        """
        other_coerced = GeneratorInt.coerce(other)
        if isinstance(other_coerced, GeneratorFloat):
            return GeneratorComparisonNEFloat(self.to_float(), other_coerced)
        return GeneratorComparisonNEInt(self, other_coerced)


# endregion

# region Wrapper Classes


@dataclass(eq=False, order=False)
class GeneratorWrapperStr(GeneratorStr, GeneratorWrapper[U, str]):
    """A Wrapper class for converting Generators to string Generators."""

    def wrap_type(self) -> type[str]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[str]: The wrapped value.
        """
        return str


@dataclass(eq=False, order=False)
class GeneratorWrapperFloat(GeneratorFloat, GeneratorWrapper[U, float]):
    """A Wrapper class for converting Generators to float Generators."""

    def wrap_type(self) -> type[float]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[float]: The wrapped value.
        """
        return float


@dataclass(eq=False, order=False)
class GeneratorWrapperInt(GeneratorInt, GeneratorWrapper[U, int]):
    """A Wrapper class for converting Generators to integer Generators."""

    def wrap_type(self) -> type[int]:
        """Get the type of the wrapper for conversion.

        Returns:
            type[int]: The wrapped value.
        """
        return int


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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


@dataclass(eq=False, order=False)
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

# region Abstract Typed Comparison Classes


@dataclass(eq=False, order=False)
class GeneratorComparisonLT(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that LT compares two Generators."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform less than comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a < b


@dataclass(eq=False, order=False)
class GeneratorComparisonLE(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that LE compares two Generators."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform less than or equal to comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a <= b


@dataclass(eq=False, order=False)
class GeneratorComparisonGT(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that GT compares two Generators."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform greater than comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a > b


@dataclass(eq=False, order=False)
class GeneratorComparisonGE(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that GE compares two Generators."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform greater than or equal to comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a >= b


@dataclass(eq=False, order=False)
class GeneratorComparisonEQ(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that compares two Generators for equality."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform equality comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a == b


@dataclass(eq=False, order=False)
class GeneratorComparisonNE(GeneratorComparison[T_SFI], GeneratorBool):
    """A Comparison Generator that compares two Generators for inequality."""

    def op(self, a: T_SFI, b: T_SFI) -> bool:
        """Perform inequality comparison on two values.

        Args:
            a (T_SFI): The first value.
            b (T_SFI): The second value.

        Returns:
            bool: The result of the operation.
        """
        return a != b


# endregion

# region Composite Classes

# region Composite Classes for Addition


@dataclass(eq=False, order=False)
class GeneratorCompositeAddStr(GeneratorStr, GeneratorCompositeAdd[str]):
    """A Composite Generator that adds two String Generators."""


@dataclass(eq=False, order=False)
class GeneratorCompositeAddFloat(GeneratorFloat, GeneratorCompositeAdd[float]):
    """A Composite Generator that adds two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorCompositeAddInt(GeneratorInt, GeneratorCompositeAdd[int]):
    """A Composite Generator that adds two Integer Generators."""


# endregion
# region Composite Classes for Subtraction


@dataclass(eq=False, order=False)
class GeneratorCompositeSubFloat(GeneratorFloat, GeneratorCompositeSub[float]):
    """A Composite Generator that subtracts two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorCompositeSubInt(GeneratorInt, GeneratorCompositeSub[int]):
    """A Composite Generator that subtracts two Integer Generators."""


# endregion
# region Composite Classes for Multiplication


@dataclass(eq=False, order=False)
class GeneratorCompositeMultFloat(GeneratorFloat, GeneratorCompositeMult[float]):
    """A Composite Generator that multiplies two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorCompositeMultInt(GeneratorInt, GeneratorCompositeMult[int]):
    """A Composite Generator that multiplies two Integer Generators."""


# endregion
# region Composite Classes for True Division


@dataclass(eq=False, order=False)
class GeneratorCompositeTrueDivFloat(GeneratorFloat, GeneratorCompositeTrueDiv[float]):
    """A Composite Generator that divides two Float Generators."""


# endregion
# region Composite Classes for Floor Division


@dataclass(eq=False, order=False)
class GeneratorCompositeFloorDivFloat(
    GeneratorFloat, GeneratorCompositeFloorDiv[float]
):
    """A Composite Generator that floor divides two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorCompositeFloorDivInt(GeneratorInt, GeneratorCompositeFloorDiv[int]):
    """A Composite Generator that floor divides two Integer Generators."""


# endregion
# region Composite Classes for And


@dataclass(eq=False, order=False)
class GeneratorCompositeAndBool(GeneratorBool, GeneratorCompositeAnd[bool]):
    """A Composite Generator that ands two Boolean Generators."""


# endregion
# region Composite Classes for Or


@dataclass(eq=False, order=False)
class GeneratorCompositeOrBool(GeneratorBool, GeneratorCompositeOr[bool]):
    """A Composite Generator that ors two Boolean Generators."""


# endregion
# region Composite Classes for Xor


@dataclass(eq=False, order=False)
class GeneratorCompositeXorBool(GeneratorBool, GeneratorCompositeXor[bool]):
    """A Composite Generator that xors two Boolean Generators."""


# endregion

# endregion

# region Comparison Classes

# region Comparison Classes for Less Than


@dataclass(eq=False, order=False)
class GeneratorComparisonLTStr(GeneratorComparisonLT[str]):
    """A Comparison Generator that LT compares two String Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonLTFloat(GeneratorComparisonLT[float]):
    """A Comparison Generator that LT compares two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonLTInt(GeneratorComparisonLT[int]):
    """A Comparison Generator that LT compares two Integer Generators."""


# endregion

# region Comparison Classes for Less Than or Equal to


@dataclass(eq=False, order=False)
class GeneratorComparisonLEStr(GeneratorComparisonLE[str]):
    """A Comparison Generator that LE compares two String Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonLEFloat(GeneratorComparisonLE[float]):
    """A Comparison Generator that LE compares two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonLEInt(GeneratorComparisonLE[int]):
    """A Comparison Generator that LE compares two Integer Generators."""


# endregion

# region Comparison Classes for Greater Than


@dataclass(eq=False, order=False)
class GeneratorComparisonGTStr(GeneratorComparisonGT[str]):
    """A Comparison Generator that GT compares two String Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonGTFloat(GeneratorComparisonGT[float]):
    """A Comparison Generator that GT compares two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonGTInt(GeneratorComparisonGT[int]):
    """A Comparison Generator that GT compares two Integer Generators."""


# endregion

# region Comparison Classes for Greater Than or Equal to


@dataclass(eq=False, order=False)
class GeneratorComparisonGEStr(GeneratorComparisonGE[str]):
    """A Comparison Generator that GE compares two String Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonGEFloat(GeneratorComparisonGE[float]):
    """A Comparison Generator that GE compares two Float Generators."""


@dataclass(eq=False, order=False)
class GeneratorComparisonGEInt(GeneratorComparisonGE[int]):
    """A Comparison Generator that GE compares two Integer Generators."""


# endregion

# region Comparison Classes for Equality


@dataclass(eq=False, order=False)
class GeneratorComparisonEQStr(GeneratorComparisonEQ[str]):
    """A Comparison Generator that compares two String Generators for equality."""


@dataclass(eq=False, order=False)
class GeneratorComparisonEQFloat(GeneratorComparisonEQ[float]):
    """A Comparison Generator that compares two Float Generators for equality."""


@dataclass(eq=False, order=False)
class GeneratorComparisonEQInt(GeneratorComparisonEQ[int]):
    """A Comparison Generator that compares two Integer Generators for equality."""


# endregion

# region Comparison Classes for Non-Equality


@dataclass(eq=False, order=False)
class GeneratorComparisonNEStr(GeneratorComparisonNE[str]):
    """A Comparison Generator that compares two String Generators for inequality."""


@dataclass(eq=False, order=False)
class GeneratorComparisonNEFloat(GeneratorComparisonNE[float]):
    """A Comparison Generator that compares two Float Generators for inequality."""


@dataclass(eq=False, order=False)
class GeneratorComparisonNEInt(GeneratorComparisonNE[int]):
    """A Comparison Generator that compares two Integer Generators for inequality."""


# endregion

# endregion

# region Constant Generators


@dataclass(eq=False, order=False)
class GeneratorConstantStr(GeneratorStr, GeneratorConstant[str]):
    """A Generator that generates a constant string value."""


@dataclass(eq=False, order=False)
class GeneratorConstantBool(GeneratorBool, GeneratorConstant[bool]):
    """A Generator that generates a constant boolean value."""


@dataclass(eq=False, order=False)
class GeneratorConstantInt(GeneratorInt, GeneratorConstant[int]):
    """A Generator that generates a constant integer value."""


@dataclass(eq=False, order=False)
class GeneratorConstantFloat(GeneratorFloat, GeneratorConstant[float]):
    """A Generator that generates a constant float value."""


# endregion

# region Types
GeneratorNumeric = Union[GeneratorInt, GeneratorFloat]
GeneratorAny = Union[GeneratorInt, GeneratorFloat, GeneratorStr, GeneratorBool]

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
GeneratorComparisonLTNumeric = Union[
    GeneratorComparisonLTInt, GeneratorComparisonLTFloat
]
GeneratorComparisonLENumeric = Union[
    GeneratorComparisonLEInt, GeneratorComparisonLEFloat
]
GeneratorComparisonGTNumeric = Union[
    GeneratorComparisonGTInt, GeneratorComparisonGTFloat
]
GeneratorComparisonGENumeric = Union[
    GeneratorComparisonGEInt, GeneratorComparisonGEFloat
]
GeneratorComparisonEQNumeric = Union[
    GeneratorComparisonEQInt, GeneratorComparisonEQFloat
]
GeneratorComparisonNENumeric = Union[
    GeneratorComparisonNEInt, GeneratorComparisonNEFloat
]


# endregion
