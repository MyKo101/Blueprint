"""Test script for the random_num module."""

from Blueprint import RandomBool
from Blueprint import RandomFloat
from Blueprint import RandomInt


def test_random_integer() -> None:
    """Test the RandomInt class."""
    x = RandomInt(0, 10)
    res = x.generate(10)
    assert isinstance(res, list)
    assert len(res) == 10
    assert all(isinstance(i, int) for i in res)
    assert all(0 <= i <= 10 for i in res)


def test_random_float() -> None:
    """Test the RandomFloat class."""
    x = RandomFloat(0, 10)
    res = x.generate(10)
    assert isinstance(res, list)
    assert len(res) == 10
    assert all(isinstance(i, float) for i in res)
    assert all(0 <= i <= 10 for i in res)


def test_random_bool() -> None:
    """Test the RandomBool class."""
    x = RandomBool(0.5)
    res = x.generate(10)
    assert isinstance(res, list)
    assert len(res) == 10
    assert all(isinstance(i, bool) for i in res)
    assert all(0 <= i <= 1 for i in res)
