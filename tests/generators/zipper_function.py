"""Test the zipper class."""

from typing import TypedDict
from typing import Union

import pytest

from Blueprint.generators import zipper


pt = Union[str, int, range]

parametrise = pytest.mark.parametrize

Args = tuple[pt, ...]
Result = tuple[tuple[pt, ...], ...]


class Payload(TypedDict):
    """Payload type."""
    args: Args
    result: Result
    length: Union[int, None]


PAYLOADS: list[Payload] = [
    {
        "args": (range(10), range(10)),
        "length": None,
        "result": ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9))
    },
    {
        "args": (range(2), 3),
        "length": None,
        "result": ((0, 3), (1, 3))
    },
    {
        "args": ("a", "b", "c", "abc"),
        "length": 5,
        "result": (("a", "b", "c", "abc"),) * 5
    }
]


class ErrPayload(TypedDict):
    """Error payload type."""
    args: Args
    length: Union[int, None]
    error: str


possible_errors = [
    "Parameter length must be greater than 0.",
    "Parameter length must match the length of provided lists.",
    "All provided lists must be the same length."
]

ERROR_PAYLOADS: list[ErrPayload] = [
    {
        "args": (0, 0),
        "length": 0,
        "error": possible_errors[0]
    },
    {
        "args": (range(10), range(10)),
        "length": -1,
        "error": possible_errors[0]
    },
    {
        "args": (range(2), 3),
        "length": 10,
        "error": possible_errors[1]
    },
    {
        "args": (range(2), range(3)),
        "length": None,
        "error": possible_errors[2]
    },
    {
        "args": (range(2), range(3), 10),
        "length": None,
        "error": possible_errors[2]
    }

]


@parametrise("payload", PAYLOADS)
def test_zipper(payload: Payload) -> None:
    """Test the zipper class."""
    args = payload["args"]
    length = payload["length"]
    result = payload["result"]

    z: zip[tuple[pt, ...]]
    if length is not None:
        z = zipper(*args, length=length)
    else:
        z = zipper(*args)
    for i, values in enumerate(z):
        assert values == result[i]


@parametrise("payload", ERROR_PAYLOADS)
def test_zipper_errors(payload: ErrPayload) -> None:
    """Test the zipper class."""
    args = payload["args"]
    length = payload["length"]
    error = payload["error"]

    with pytest.raises(ValueError) as excinfo:
        if length is not None:
            zipper(*args, length=length)
        else:
            zipper(*args)
    assert str(excinfo.value) == error
