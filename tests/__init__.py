"""Test suite for the Blueprint package."""

import Blueprint


def test_dummy() -> None:
    """Dummy test.

    Returns:
        None
    """
    x = Blueprint.RandomInt(0, 10)
    res = x.generate(10)
    assert all(0 <= i <= 10 for i in res)

    return None
