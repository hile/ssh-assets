"""
Unit tests for ssh_assets.duration module
"""
from datetime import timedelta

import pytest

from ssh_assets.duration import Duration

from .conftest import VALID_DURATION_VALUES


def test_duration_invalid_values(invalid_duration_value):
    """
    Test parsing invalid duration string values. Each invalid value must raise ValueError
    """
    with pytest.raises(ValueError):
        Duration(invalid_duration_value)


def test_duration_valid_values(valid_duration_value):
    """
    Test parsing valid duration string values
    """
    duration = Duration(valid_duration_value)
    assert isinstance(duration.__repr__(), str)
    assert isinstance(duration.timedelta, timedelta)


def test_duration_valid_value_compare():
    """
    Test comparing two valid duration values
    """
    a = Duration(VALID_DURATION_VALUES[0])
    b = Duration(VALID_DURATION_VALUES[1])

    assert a == a  # pylint: disable=comparison-with-itself
    assert not a != a    # pylint: disable=comparison-with-itself,unneeded-not
    assert a != b

    assert a < b
    assert b > a
    assert a <= a  # pylint: disable=comparison-with-itself
    assert b >= b  # pylint: disable=comparison-with-itself
