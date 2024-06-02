"""Test generator constants."""

import math as maths
from typing import TypedDict
from typing import Union

import pytest

from Blueprint.generators import to_generator
from Blueprint.generators.generators import GeneratorConstantBool
from Blueprint.generators.generators import GeneratorConstantFloat
from Blueprint.generators.generators import GeneratorConstantInt
from Blueprint.generators.generators import GeneratorConstantStr


parametrise = pytest.mark.parametrize

types = Union[bool, int, float, str]


class Payload(TypedDict):
    """Payload type."""

    value: types
    result: Union[
        GeneratorConstantBool,
        GeneratorConstantInt,
        GeneratorConstantFloat,
        GeneratorConstantStr,
    ]


PAYLOADS: list[Payload] = [
    {
        "value": True,
        "result": GeneratorConstantBool(True),
    },
    {
        "value": False,
        "result": GeneratorConstantBool(False),
    },
    {
        "value": 1,
        "result": GeneratorConstantInt(1),
    },
    {
        "value": -30,
        "result": GeneratorConstantInt(-30),
    },
    {
        "value": maths.inf,
        "result": GeneratorConstantFloat(maths.inf),
    },
    {
        "value": "a",
        "result": GeneratorConstantStr("a"),
    },
    {
        "value": "hello",
        "result": GeneratorConstantStr("hello"),
    },
]


@parametrise("payload", PAYLOADS)
def test_constant(payload: Payload) -> None:
    """Test the constant generator."""
    observed = to_generator(payload["value"])
    expected = payload["result"]

    assert observed.value == expected.value
    return None
