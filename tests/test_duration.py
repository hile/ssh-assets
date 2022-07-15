"""
Unit tests for ssh_assets.duration module
"""
from datetime import timedelta

import pytest

from ssh_assets.duration import Duration


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
