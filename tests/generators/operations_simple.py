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
from Blueprint.generators.generators import GeneratorCompositeAddFloat
from Blueprint.generators.generators import GeneratorCompositeAddInt
from Blueprint.generators.generators import GeneratorCompositeAddStr
from Blueprint.generators.generators import GeneratorCompositeAndBool
from Blueprint.generators.generators import GeneratorCompositeFloorDivFloat
from Blueprint.generators.generators import GeneratorCompositeFloorDivInt
from Blueprint.generators.generators import GeneratorCompositeMultFloat
from Blueprint.generators.generators import GeneratorCompositeMultInt
from Blueprint.generators.generators import GeneratorCompositeOrBool
from Blueprint.generators.generators import GeneratorCompositeSubFloat
from Blueprint.generators.generators import GeneratorCompositeSubInt
from Blueprint.generators.generators import GeneratorCompositeTrueDivFloat
from Blueprint.generators.generators import GeneratorCompositeXorBool
from Blueprint.generators.generators import GeneratorFloat
from Blueprint.generators.generators import GeneratorInt
from Blueprint.generators.generators import GeneratorStr


parametrise = pytest.mark.parametrize

T = TypeVar("T", float, float, bool, str)


class Payload(TypedDict, Generic[T]):
    """Payload type."""

    left: T
    right: T
    result: T


class PayloadFloat(Payload[float]):
    """Payload type for floats."""

    operation: Literal["add", "sub", "mul", "fdiv", "div"]


class PayloadInt(Payload[int]):
    """Payload type for ints."""

    operation: Literal["add", "sub", "mul", "fdiv", "div"]


class PayloadStr(Payload[str]):
    """Payload type for strings."""

    operation: Literal["add"]


class PayloadBool(Payload[bool]):
    """Payload type for bools."""

    operation: Literal["and", "or", "xor"]


class PayloadIntFloat(TypedDict):
    """Payload type for ints and floats."""

    left: Union[int, float]
    right: Union[int, float]
    result: float
    operation: Literal["add", "sub", "mul", "fdiv", "div"]


PAYLOADS_FLOAT: list[PayloadFloat] = [
    {"left": 1.0, "right": 1.0, "result": 2.0, "operation": "add"},
    {"left": 1.0, "right": 1.0, "result": 0.0, "operation": "sub"},
    {"left": 1.0, "right": 1.0, "result": 1.0, "operation": "mul"},
    {"left": 1.0, "right": 1.0, "result": 1.0, "operation": "fdiv"},
    {"left": 1.0, "right": 1.0, "result": 1.0, "operation": "div"},
    {"left": 1.0, "right": 2.0, "result": 3.0, "operation": "add"},
    {"left": 1.0, "right": 2.0, "result": -1.0, "operation": "sub"},
    {"left": 1.0, "right": 2.0, "result": 2.0, "operation": "mul"},
    {"left": 1.0, "right": 2.0, "result": 0.0, "operation": "fdiv"},
    {"left": 1.0, "right": 2.0, "result": 0.5, "operation": "div"},
    {"left": 1.0, "right": -10.0, "result": -9.0, "operation": "add"},
    {"left": 1.0, "right": -10.0, "result": 11.0, "operation": "sub"},
    {"left": 1.0, "right": -10.0, "result": -10.0, "operation": "mul"},
    {"left": 1.0, "right": -10.0, "result": -1.0, "operation": "fdiv"},
    {"left": 1.0, "right": -10.0, "result": -0.1, "operation": "div"},
    {"left": 2.0, "right": 1.0, "result": 3.0, "operation": "add"},
    {"left": 2.0, "right": 1.0, "result": 1.0, "operation": "sub"},
    {"left": 2.0, "right": 1.0, "result": 2.0, "operation": "mul"},
    {"left": 2.0, "right": 1.0, "result": 2.0, "operation": "fdiv"},
    {"left": 2.0, "right": 1.0, "result": 2.0, "operation": "div"},
    {"left": 2.0, "right": 2.0, "result": 4.0, "operation": "add"},
    {"left": 2.0, "right": 2.0, "result": 0.0, "operation": "sub"},
    {"left": 2.0, "right": 2.0, "result": 4.0, "operation": "mul"},
    {"left": 2.0, "right": 2.0, "result": 1.0, "operation": "fdiv"},
    {"left": 2.0, "right": 2.0, "result": 1.0, "operation": "div"},
    {"left": 2.0, "right": -10.0, "result": -8.0, "operation": "add"},
    {"left": 2.0, "right": -10.0, "result": 12.0, "operation": "sub"},
    {"left": 2.0, "right": -10.0, "result": -20.0, "operation": "mul"},
    {"left": 2.0, "right": -10.0, "result": -1.0, "operation": "fdiv"},
    {"left": 2.0, "right": -10.0, "result": -0.2, "operation": "div"},
    {"left": -10.0, "right": 1.0, "result": -9.0, "operation": "add"},
    {"left": -10.0, "right": 1.0, "result": -11.0, "operation": "sub"},
    {"left": -10.0, "right": 1.0, "result": -10.0, "operation": "mul"},
    {"left": -10.0, "right": 1.0, "result": -10.0, "operation": "fdiv"},
    {"left": -10.0, "right": 1.0, "result": -10.0, "operation": "div"},
    {"left": -10.0, "right": 2.0, "result": -8.0, "operation": "add"},
    {"left": -10.0, "right": 2.0, "result": -12.0, "operation": "sub"},
    {"left": -10.0, "right": 2.0, "result": -20.0, "operation": "mul"},
    {"left": -10.0, "right": 2.0, "result": -5.0, "operation": "fdiv"},
    {"left": -10.0, "right": 2.0, "result": -5.0, "operation": "div"},
    {"left": -10.0, "right": -10.0, "result": -20.0, "operation": "add"},
    {"left": -10.0, "right": -10.0, "result": 0.0, "operation": "sub"},
    {"left": -10.0, "right": -10.0, "result": 100.0, "operation": "mul"},
    {"left": -10.0, "right": -10.0, "result": 1.0, "operation": "fdiv"},
    {"left": -10.0, "right": -10.0, "result": 1.0, "operation": "div"},
]


PAYLOADS_INT: list[PayloadInt] = [
    {"left": 1, "right": 1, "result": 2, "operation": "add"},
    {"left": 1, "right": 1, "result": 0, "operation": "sub"},
    {"left": 1, "right": 1, "result": 1, "operation": "mul"},
    {"left": 1, "right": 1, "result": 1, "operation": "fdiv"},
    {"left": 1, "right": 2, "result": 3, "operation": "add"},
    {"left": 1, "right": 2, "result": -1, "operation": "sub"},
    {"left": 1, "right": 2, "result": 2, "operation": "mul"},
    {"left": 1, "right": 2, "result": 0, "operation": "fdiv"},
    {"left": 1, "right": -10, "result": -9, "operation": "add"},
    {"left": 1, "right": -10, "result": 11, "operation": "sub"},
    {"left": 1, "right": -10, "result": -10, "operation": "mul"},
    {"left": 1, "right": -10, "result": -1, "operation": "fdiv"},
    {"left": 2, "right": 1, "result": 3, "operation": "add"},
    {"left": 2, "right": 1, "result": 1, "operation": "sub"},
    {"left": 2, "right": 1, "result": 2, "operation": "mul"},
    {"left": 2, "right": 1, "result": 2, "operation": "fdiv"},
    {"left": 2, "right": 1, "result": 2, "operation": "div"},
    {"left": 2, "right": 2, "result": 4, "operation": "add"},
    {"left": 2, "right": 2, "result": 0, "operation": "sub"},
    {"left": 2, "right": 2, "result": 4, "operation": "mul"},
    {"left": 2, "right": 2, "result": 1, "operation": "fdiv"},
    {"left": 2, "right": 2, "result": 1, "operation": "div"},
    {"left": 2, "right": -10, "result": -8, "operation": "add"},
    {"left": 2, "right": -10, "result": 12, "operation": "sub"},
    {"left": 2, "right": -10, "result": -20, "operation": "mul"},
    {"left": 2, "right": -10, "result": -1, "operation": "fdiv"},
    {"left": -10, "right": 1, "result": -9, "operation": "add"},
    {"left": -10, "right": 1, "result": -11, "operation": "sub"},
    {"left": -10, "right": 1, "result": -10, "operation": "mul"},
    {"left": -10, "right": 1, "result": -10, "operation": "fdiv"},
    {"left": -10, "right": 1, "result": -10, "operation": "div"},
    {"left": -10, "right": 2, "result": -8, "operation": "add"},
    {"left": -10, "right": 2, "result": -12, "operation": "sub"},
    {"left": -10, "right": 2, "result": -20, "operation": "mul"},
    {"left": -10, "right": 2, "result": -5, "operation": "fdiv"},
    {"left": -10, "right": 2, "result": -5, "operation": "div"},
    {"left": -10, "right": -10, "result": -20, "operation": "add"},
    {"left": -10, "right": -10, "result": 0, "operation": "sub"},
    {"left": -10, "right": -10, "result": 100, "operation": "mul"},
    {"left": -10, "right": -10, "result": 1, "operation": "fdiv"},
    {"left": -10, "right": -10, "result": 1, "operation": "div"},
]

PAYLOADS_STR: list[PayloadStr] = [
    {"left": "a", "right": "a", "result": "aa", "operation": "add"},
    {"left": "a", "right": "b", "result": "ab", "operation": "add"},
    {"left": "b", "right": "a", "result": "ba", "operation": "add"},
    {"left": "b", "right": "b", "result": "bb", "operation": "add"},
]

PAYLOADS_BOOL: list[PayloadBool] = [
    {"left": True, "right": True, "result": True, "operation": "and"},
    {"left": True, "right": True, "result": True, "operation": "or"},
    {"left": True, "right": True, "result": False, "operation": "xor"},
    {"left": True, "right": False, "result": False, "operation": "and"},
    {"left": True, "right": False, "result": True, "operation": "or"},
    {"left": True, "right": False, "result": True, "operation": "xor"},
    {"left": False, "right": True, "result": False, "operation": "and"},
    {"left": False, "right": True, "result": True, "operation": "or"},
    {"left": False, "right": True, "result": True, "operation": "xor"},
    {"left": False, "right": False, "result": False, "operation": "and"},
    {"left": False, "right": False, "result": False, "operation": "or"},
    {"left": False, "right": False, "result": False, "operation": "xor"},
]

PAYLOADS_INT_FLOAT: list[PayloadIntFloat] = [
    {"left": 1, "right": 1.0, "result": 2.0, "operation": "add"},
    {"left": 1.0, "right": 1, "result": 2.0, "operation": "add"},
    {"left": 1, "right": 1.0, "result": 0.0, "operation": "sub"},
    {"left": 1.0, "right": 1, "result": 0.0, "operation": "sub"},
    {"left": 1, "right": 1.0, "result": 1.0, "operation": "mul"},
    {"left": 1.0, "right": 1, "result": 1.0, "operation": "mul"},
    {"left": 1, "right": 1.0, "result": 1.0, "operation": "fdiv"},
    {"left": 1.0, "right": 1, "result": 1.0, "operation": "fdiv"},
    {"left": 1, "right": 1.0, "result": 1.0, "operation": "div"},
    {"left": 1.0, "right": 1, "result": 1.0, "operation": "div"},
    {"left": 1, "right": 2.0, "result": 3.0, "operation": "add"},
    {"left": 1.0, "right": 2, "result": 3.0, "operation": "add"},
    {"left": 1, "right": 2.0, "result": -1.0, "operation": "sub"},
    {"left": 1.0, "right": 2, "result": -1.0, "operation": "sub"},
    {"left": 1, "right": 2.0, "result": 2.0, "operation": "mul"},
    {"left": 1.0, "right": 2, "result": 2.0, "operation": "mul"},
    {"left": 1, "right": 2.0, "result": 0.0, "operation": "fdiv"},
    {"left": 1.0, "right": 2, "result": 0.0, "operation": "fdiv"},
    {"left": 1, "right": 2.0, "result": 0.5, "operation": "div"},
    {"left": 1.0, "right": 2, "result": 0.5, "operation": "div"},
    {"left": 2, "right": 1.0, "result": 3.0, "operation": "add"},
    {"left": 2.0, "right": 1, "result": 3.0, "operation": "add"},
    {"left": 2, "right": 1.0, "result": 1.0, "operation": "sub"},
    {"left": 2.0, "right": 1, "result": 1.0, "operation": "sub"},
    {"left": 2, "right": 1.0, "result": 2.0, "operation": "mul"},
    {"left": 2.0, "right": 1, "result": 2.0, "operation": "mul"},
    {"left": 2, "right": 1.0, "result": 2.0, "operation": "fdiv"},
    {"left": 2.0, "right": 1, "result": 2.0, "operation": "fdiv"},
    {"left": 2, "right": 1.0, "result": 2.0, "operation": "div"},
    {"left": 2.0, "right": 1, "result": 2.0, "operation": "div"},
    {"left": 2, "right": 2.0, "result": 4.0, "operation": "add"},
    {"left": 2.0, "right": 2, "result": 4.0, "operation": "add"},
    {"left": 2, "right": 2.0, "result": 0.0, "operation": "sub"},
    {"left": 2.0, "right": 2, "result": 0.0, "operation": "sub"},
    {"left": 2, "right": 2.0, "result": 4.0, "operation": "mul"},
    {"left": 2.0, "right": 2, "result": 4.0, "operation": "mul"},
    {"left": 2, "right": 2.0, "result": 1.0, "operation": "fdiv"},
    {"left": 2.0, "right": 2, "result": 1.0, "operation": "fdiv"},
    {"left": 2, "right": 2.0, "result": 1.0, "operation": "div"},
    {"left": 2.0, "right": 2, "result": 1.0, "operation": "div"},
]


@parametrise("payload", PAYLOADS_FLOAT)
def test_float(payload: PayloadFloat) -> None:
    """Test float binary operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorFloat
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddFloat)
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubFloat)
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultFloat)
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivFloat)
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_FLOAT)
def test_float_coerce(payload: PayloadFloat) -> None:
    """Test float binary operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorFloat
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddFloat)
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubFloat)
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultFloat)
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivFloat)
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT)
def test_int(payload: PayloadInt) -> None:
    """Test int binary operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: Union[GeneratorInt, GeneratorFloat]
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddInt) or isinstance(
            observed, GeneratorCompositeAddFloat
        )
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubInt) or isinstance(
            observed, GeneratorCompositeSubFloat
        )
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultInt) or isinstance(
            observed, GeneratorCompositeMultFloat
        )
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivInt) or isinstance(
            observed, GeneratorCompositeFloorDivFloat
        )
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorInt) or isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT)
def test_int_coerce(payload: PayloadInt) -> None:
    """Test int binary operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: Union[GeneratorInt, GeneratorFloat]
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddInt) or isinstance(
            observed, GeneratorCompositeAddFloat
        )
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubInt) or isinstance(
            observed, GeneratorCompositeSubFloat
        )
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultInt) or isinstance(
            observed, GeneratorCompositeMultFloat
        )
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivInt) or isinstance(
            observed, GeneratorCompositeFloorDivFloat
        )
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorInt) or isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_STR)
def test_str(payload: PayloadStr) -> None:
    """Test str concatenation."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorStr
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddStr)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorStr)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_STR)
def test_str_coerce(payload: PayloadStr) -> None:
    """Test str concatenation with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorStr
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddStr)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorStr)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_BOOL)
def test_bool(payload: PayloadBool) -> None:
    """Test bool binary operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "and":
        observed = left & right
        assert isinstance(observed, GeneratorCompositeAndBool)
    elif operation == "or":
        observed = left | right
        assert isinstance(observed, GeneratorCompositeOrBool)
    elif operation == "xor":
        observed = left ^ right
        assert isinstance(observed, GeneratorCompositeXorBool)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_BOOL)
def test_bool_coerce(payload: PayloadBool) -> None:
    """Test bool binary operations with coercion."""
    left = to_generator(payload["left"])
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: GeneratorBool
    if operation == "and":
        observed = left & right
        assert isinstance(observed, GeneratorCompositeAndBool)
    elif operation == "or":
        observed = left | right
        assert isinstance(observed, GeneratorCompositeOrBool)
    elif operation == "xor":
        observed = left ^ right
        assert isinstance(observed, GeneratorCompositeXorBool)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorBool)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT_FLOAT)
def test_int_float(payload: PayloadIntFloat) -> None:
    """Test int and float binary operations."""
    left = to_generator(payload["left"])
    right = to_generator(payload["right"])
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: Union[GeneratorFloat, GeneratorInt]
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddInt) or isinstance(
            observed, GeneratorCompositeAddFloat
        )
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubInt) or isinstance(
            observed, GeneratorCompositeSubFloat
        )
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultInt) or isinstance(
            observed, GeneratorCompositeMultFloat
        )
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivInt) or isinstance(
            observed, GeneratorCompositeFloorDivFloat
        )
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorInt) or isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)


@parametrise("payload", PAYLOADS_INT_FLOAT)
def test_int_float_coerce(payload: PayloadIntFloat) -> None:
    """Test int and float binary operations with coercion."""
    payload_left = payload["left"]
    left = to_generator(payload_left)
    right = payload["right"]
    expected = to_generator(payload["result"])
    operation = payload["operation"]
    observed: Union[GeneratorFloat, GeneratorInt]
    if operation == "add":
        observed = left + right
        assert isinstance(observed, GeneratorCompositeAddInt) or isinstance(
            observed, GeneratorCompositeAddFloat
        )
    elif operation == "sub":
        observed = left - right
        assert isinstance(observed, GeneratorCompositeSubInt) or isinstance(
            observed, GeneratorCompositeSubFloat
        )
    elif operation == "mul":
        observed = left * right
        assert isinstance(observed, GeneratorCompositeMultInt) or isinstance(
            observed, GeneratorCompositeMultFloat
        )
    elif operation == "fdiv":
        observed = left // right
        assert isinstance(observed, GeneratorCompositeFloorDivInt) or isinstance(
            observed, GeneratorCompositeFloorDivFloat
        )
    elif operation == "div":
        observed = left / right
        assert isinstance(observed, GeneratorCompositeTrueDivFloat)
    else:
        assert_never(operation)

    assert isinstance(observed, GeneratorInt) or isinstance(observed, GeneratorFloat)
    assert observed.generate(1) == expected.generate(1)
