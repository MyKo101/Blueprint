"""Test generator operations."""

from typing import Generic
from typing import Literal
from typing import TypeVar
from typing import Union

import pytest
from typing_extensions import TypedDict
from typing_extensions import assert_never

from Blueprint.generators import to_generator
from Blueprint.generators.generators import GeneratorBool
from Blueprint.generators.generators import GeneratorComparisonEQFloat
from Blueprint.generators.generators import GeneratorComparisonEQInt
from Blueprint.generators.generators import GeneratorComparisonEQStr
from Blueprint.generators.generators import GeneratorComparisonGEFloat
from Blueprint.generators.generators import GeneratorComparisonGEInt
from Blueprint.generators.generators import GeneratorComparisonGEStr
from Blueprint.generators.generators import GeneratorComparisonGTFloat
from Blueprint.generators.generators import GeneratorComparisonGTInt
from Blueprint.generators.generators import GeneratorComparisonGTStr
from Blueprint.generators.generators import GeneratorComparisonLEFloat
from Blueprint.generators.generators import GeneratorComparisonLEInt
from Blueprint.generators.generators import GeneratorComparisonLEStr
from Blueprint.generators.generators import GeneratorComparisonLTFloat
from Blueprint.generators.generators import GeneratorComparisonLTInt
from Blueprint.generators.generators import GeneratorComparisonLTStr
from Blueprint.generators.generators import GeneratorComparisonNEFloat
from Blueprint.generators.generators import GeneratorComparisonNEInt
from Blueprint.generators.generators import GeneratorComparisonNEStr


parametrise = pytest.mark.parametrize

T = TypeVar("T", float, int, str)


class Payload(TypedDict, Generic[T]):
    """Payload type."""

    left: T
    right: T
    result: bool
    operation: Literal["lt", "le", "gt", "ge", "eq", "ne"]


class PayloadIntFloat(TypedDict):
    """Payload type for ints and floats."""

    left: Union[int, float]
    right: Union[int, float]
    result: bool
    operation: Literal["lt", "le", "gt", "ge", "eq", "ne"]


PAYLOADS_FLOAT: list[Payload[float]] = [
    {"left": 1.0, "right": 1.0, "result": False, "operation": "lt"},
    {"left": 1.0, "right": 1.0, "result": True, "operation": "le"},
    {"left": 1.0, "right": 1.0, "result": False, "operation": "gt"},
    {"left": 1.0, "right": 1.0, "result": True, "operation": "ge"},
    {"left": 1.0, "right": 1.0, "result": True, "operation": "eq"},
    {"left": 1.0, "right": 1.0, "result": False, "operation": "ne"},
    {"left": 1.0, "right": 2.0, "result": True, "operation": "lt"},
    {"left": 1.0, "right": 2.0, "result": True, "operation": "le"},
    {"left": 1.0, "right": 2.0, "result": False, "operation": "gt"},
    {"left": 1.0, "right": 2.0, "result": False, "operation": "ge"},
    {"left": 1.0, "right": 2.0, "result": False, "operation": "eq"},
    {"left": 1.0, "right": 2.0, "result": True, "operation": "ne"},
    {"left": 2.0, "right": 1.0, "result": False, "operation": "lt"},
    {"left": 2.0, "right": 1.0, "result": False, "operation": "le"},
    {"left": 2.0, "right": 1.0, "result": True, "operation": "gt"},
    {"left": 2.0, "right": 1.0, "result": True, "operation": "ge"},
    {"left": 2.0, "right": 1.0, "result": False, "operation": "eq"},
    {"left": 2.0, "right": 1.0, "result": True, "operation": "ne"},
    {"left": 2.0, "right": 2.0, "result": False, "operation": "lt"},
    {"left": 2.0, "right": 2.0, "result": True, "operation": "le"},
    {"left": 2.0, "right": 2.0, "result": False, "operation": "gt"},
    {"left": 2.0, "right": 2.0, "result": True, "operation": "ge"},
    {"left": 2.0, "right": 2.0, "result": True, "operation": "eq"},
    {"left": 2.0, "right": 2.0, "result": False, "operation": "ne"},
]


PAYLOADS_INT: list[Payload[int]] = [
    {"left": 1, "right": 1, "result": False, "operation": "lt"},
    {"left": 1, "right": 1, "result": True, "operation": "le"},
    {"left": 1, "right": 1, "result": False, "operation": "gt"},
    {"left": 1, "right": 1, "result": True, "operation": "ge"},
    {"left": 1, "right": 1, "result": True, "operation": "eq"},
    {"left": 1, "right": 1, "result": False, "operation": "ne"},
    {"left": 1, "right": 2, "result": True, "operation": "lt"},
    {"left": 1, "right": 2, "result": True, "operation": "le"},
    {"left": 1, "right": 2, "result": False, "operation": "gt"},
    {"left": 1, "right": 2, "result": False, "operation": "ge"},
    {"left": 1, "right": 2, "result": False, "operation": "eq"},
    {"left": 1, "right": 2, "result": True, "operation": "ne"},
    {"left": 2, "right": 1, "result": False, "operation": "lt"},
    {"left": 2, "right": 1, "result": False, "operation": "le"},
    {"left": 2, "right": 1, "result": True, "operation": "gt"},
    {"left": 2, "right": 1, "result": True, "operation": "ge"},
    {"left": 2, "right": 1, "result": False, "operation": "eq"},
    {"left": 2, "right": 1, "result": True, "operation": "ne"},
    {"left": 2, "right": 2, "result": False, "operation": "lt"},
    {"left": 2, "right": 2, "result": True, "operation": "le"},
    {"left": 2, "right": 2, "result": False, "operation": "gt"},
    {"left": 2, "right": 2, "result": True, "operation": "ge"},
    {"left": 2, "right": 2, "result": True, "operation": "eq"},
    {"left": 2, "right": 2, "result": False, "operation": "ne"},
]

PAYLOADS_STR: list[Payload[str]] = [
    {"left": "a", "right": "a", "result": False, "operation": "lt"},
    {"left": "a", "right": "a", "result": True, "operation": "le"},
    {"left": "a", "right": "a", "result": False, "operation": "gt"},
    {"left": "a", "right": "a", "result": True, "operation": "ge"},
    {"left": "a", "right": "a", "result": True, "operation": "eq"},
    {"left": "a", "right": "a", "result": False, "operation": "ne"},
    {"left": "a", "right": "b", "result": True, "operation": "lt"},
    {"left": "a", "right": "b", "result": True, "operation": "le"},
    {"left": "a", "right": "b", "result": False, "operation": "gt"},
    {"left": "a", "right": "b", "result": False, "operation": "ge"},
    {"left": "a", "right": "b", "result": False, "operation": "eq"},
    {"left": "a", "right": "b", "result": True, "operation": "ne"},
    {"left": "b", "right": "a", "result": False, "operation": "lt"},
    {"left": "b", "right": "a", "result": False, "operation": "le"},
    {"left": "b", "right": "a", "result": True, "operation": "gt"},
    {"left": "b", "right": "a", "result": True, "operation": "ge"},
    {"left": "b", "right": "a", "result": False, "operation": "eq"},
    {"left": "b", "right": "a", "result": True, "operation": "ne"},
    {"left": "b", "right": "b", "result": False, "operation": "lt"},
    {"left": "b", "right": "b", "result": True, "operation": "le"},
    {"left": "b", "right": "b", "result": False, "operation": "gt"},
    {"left": "b", "right": "b", "result": True, "operation": "ge"},
    {"left": "b", "right": "b", "result": True, "operation": "eq"},
    {"left": "b", "right": "b", "result": False, "operation": "ne"},
]

PAYLOADS_INT_FLOAT: list[PayloadIntFloat] = [
    {"left": 1, "right": 1, "result": False, "operation": "lt"},
    {"left": 1, "right": 1, "result": True, "operation": "le"},
    {"left": 1, "right": 1, "result": False, "operation": "gt"},
    {"left": 1, "right": 1, "result": True, "operation": "ge"},
    {"left": 1, "right": 1, "result": True, "operation": "eq"},
    {"left": 1, "right": 1, "result": False, "operation": "ne"},
    {"left": 1, "right": 2, "result": True, "operation": "lt"},
    {"left": 1, "right": 2, "result": True, "operation": "le"},
    {"left": 1, "right": 2, "result": False, "operation": "gt"},
    {"left": 1, "right": 2, "result": False, "operation": "ge"},
    {"left": 1, "right": 2, "result": False, "operation": "eq"},
    {"left": 1, "right": 2, "result": True, "operation": "ne"},
    {"left": 2, "right": 1, "result": False, "operation": "lt"},
    {"left": 2, "right": 1, "result": False, "operation": "le"},
    {"left": 2, "right": 1, "result": True, "operation": "gt"},
    {"left": 2, "right": 1, "result": True, "operation": "ge"},
    {"left": 2, "right": 1, "result": False, "operation": "eq"},
    {"left": 2, "right": 1, "result": True, "operation": "ne"},
    {"left": 2, "right": 2, "result": False, "operation": "lt"},
    {"left": 2, "right": 2, "result": True, "operation": "le"},
    {"left": 2, "right": 2, "result": False, "operation": "gt"},
    {"left": 2, "right": 2, "result": True, "operation": "ge"},
    {"left": 2, "right": 2, "result": True, "operation": "eq"},
    {"left": 2, "right": 2, "result": False, "operation": "ne"},
    {"left": 1.0, "right": 1, "result": False, "operation": "lt"},
    {"left": 1, "right": 1.0, "result": False, "operation": "lt"},
    {"left": 1.0, "right": 1, "result": True, "operation": "le"},
    {"left": 1, "right": 1.0, "result": True, "operation": "le"},
    {"left": 1.0, "right": 1, "result": False, "operation": "gt"},
    {"left": 1, "right": 1.0, "result": False, "operation": "gt"},
    {"left": 1.0, "right": 1, "result": True, "operation": "ge"},
    {"left": 1, "right": 1.0, "result": True, "operation": "ge"},
    {"left": 1.0, "right": 1, "result": True, "operation": "eq"},
    {"left": 1, "right": 1.0, "result": True, "operation": "eq"},
    {"left": 1.0, "right": 1, "result": False, "operation": "ne"},
    {"left": 1, "right": 1.0, "result": False, "operation": "ne"},
    {"left": 1.0, "right": 2, "result": True, "operation": "lt"},
    {"left": 1, "right": 2.0, "result": True, "operation": "lt"},
    {"left": 1.0, "right": 2, "result": True, "operation": "le"},
    {"left": 1, "right": 2.0, "result": True, "operation": "le"},
    {"left": 1.0, "right": 2, "result": False, "operation": "gt"},
    {"left": 1, "right": 2.0, "result": False, "operation": "gt"},
    {"left": 1.0, "right": 2, "result": False, "operation": "ge"},
    {"left": 1, "right": 2.0, "result": False, "operation": "ge"},
    {"left": 1.0, "right": 2, "result": False, "operation": "eq"},
    {"left": 1, "right": 2.0, "result": False, "operation": "eq"},
    {"left": 1.0, "right": 2, "result": True, "operation": "ne"},
    {"left": 1, "right": 2.0, "result": True, "operation": "ne"},
    {"left": 2.0, "right": 1, "result": False, "operation": "lt"},
    {"left": 2, "right": 1.0, "result": False, "operation": "lt"},
    {"left": 2.0, "right": 1, "result": False, "operation": "le"},
    {"left": 2, "right": 1.0, "result": False, "operation": "le"},
    {"left": 2.0, "right": 1, "result": True, "operation": "gt"},
    {"left": 2, "right": 1.0, "result": True, "operation": "gt"},
    {"left": 2.0, "right": 1, "result": True, "operation": "ge"},
    {"left": 2, "right": 1.0, "result": True, "operation": "ge"},
    {"left": 2.0, "right": 1, "result": False, "operation": "eq"},
    {"left": 2, "right": 1.0, "result": False, "operation": "eq"},
    {"left": 2.0, "right": 1, "result": True, "operation": "ne"},
    {"left": 2, "right": 1.0, "result": True, "operation": "ne"},
    {"left": 2.0, "right": 2, "result": False, "operation": "lt"},
    {"left": 2, "right": 2.0, "result": False, "operation": "lt"},
    {"left": 2.0, "right": 2, "result": True, "operation": "le"},
    {"left": 2, "right": 2.0, "result": True, "operation": "le"},
    {"left": 2.0, "right": 2, "result": False, "operation": "gt"},
    {"left": 2, "right": 2.0, "result": False, "operation": "gt"},
    {"left": 2.0, "right": 2, "result": True, "operation": "ge"},
    {"left": 2, "right": 2.0, "result": True, "operation": "ge"},
    {"left": 2.0, "right": 2, "result": True, "operation": "eq"},
    {"left": 2, "right": 2.0, "result": True, "operation": "eq"},
    {"left": 2.0, "right": 2, "result": False, "operation": "ne"},
    {"left": 2, "right": 2.0, "result": False, "operation": "ne"},
]


@parametrise("payload", PAYLOADS_FLOAT)
def test_float(payload: Payload[float]) -> None:
    """Test float comparison operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTFloat)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEFloat)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTFloat)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEFloat)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQFloat)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEFloat)
    else:
        assert_never(operation)

    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_FLOAT)
def test_float_coerce(payload: Payload[float]) -> None:
    """Test float comparison operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTFloat)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEFloat)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTFloat)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEFloat)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQFloat)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEFloat)
    else:
        assert_never(operation)
    assert isinstance(observed, GeneratorBool)

    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT)
def test_int(payload: Payload[int]) -> None:
    """Test int comparison operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTInt)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEInt)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTInt)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEInt)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQInt)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEInt)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT)
def test_int_coerce(payload: Payload[int]) -> None:
    """Test int comparison operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTInt)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEInt)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTInt)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEInt)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQInt)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEInt)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_STR)
def test_str(payload: Payload[str]) -> None:
    """Test str comparison operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTStr)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEStr)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTStr)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEStr)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQStr)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEStr)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_STR)
def test_str_coerce(payload: Payload[str]) -> None:
    """Test str comparison operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTStr)
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEStr)
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTStr)
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEStr)
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQStr)
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEStr)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT_FLOAT)
def test_int_float(payload: PayloadIntFloat) -> None:
    """Test int comparison operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTInt) or isinstance(
            observed, GeneratorComparisonLTFloat
        )
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEInt) or isinstance(
            observed, GeneratorComparisonLEFloat
        )
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTInt) or isinstance(
            observed, GeneratorComparisonGTFloat
        )
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEInt) or isinstance(
            observed, GeneratorComparisonGEFloat
        )
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQInt) or isinstance(
            observed, GeneratorComparisonEQFloat
        )
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEInt) or isinstance(
            observed, GeneratorComparisonNEFloat
        )
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT_FLOAT)
def test_int_float_coerce(payload: PayloadIntFloat) -> None:
    """Test int comparison operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "lt":
        observed = left < right
        assert isinstance(observed, GeneratorComparisonLTInt) or isinstance(
            observed, GeneratorComparisonLTFloat
        )
    elif operation == "le":
        observed = left <= right
        assert isinstance(observed, GeneratorComparisonLEInt) or isinstance(
            observed, GeneratorComparisonLEFloat
        )
    elif operation == "gt":
        observed = left > right
        assert isinstance(observed, GeneratorComparisonGTInt) or isinstance(
            observed, GeneratorComparisonGTFloat
        )
    elif operation == "ge":
        observed = left >= right
        assert isinstance(observed, GeneratorComparisonGEInt) or isinstance(
            observed, GeneratorComparisonGEFloat
        )
    elif operation == "eq":
        observed = left == right
        assert isinstance(observed, GeneratorComparisonEQInt) or isinstance(
            observed, GeneratorComparisonEQFloat
        )
    elif operation == "ne":
        observed = left != right
        assert isinstance(observed, GeneratorComparisonNEInt) or isinstance(
            observed, GeneratorComparisonNEFloat
        )
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)
