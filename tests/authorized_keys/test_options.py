#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.authorized_keys.options module
"""
import pytest

from ssh_assets.exceptions import SSHKeyError

from ssh_assets.authorized_keys.constants import (
    AUTHRORIZED_KEYS_OPTION_FLAGS,
    AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS,
)
from ssh_assets.authorized_keys.options import (
    AuthorizedKeyOptionFlag,
    AuthorizedKeyOptionValue,
    parse_option_flag,
)

DUMMY_VALUE = 'foo=bar baz=zyxxy'
MOCK_INVALID_SIMPLE_FLAG_NAME = 'foo,command="echo yeah"'
MOCK_INVALID_VALUE_FLAG_NAME = 'myflag="foo bar"'
MOCK_INVALID_FLAG_VALUE = 'command="echo "yeah"",pty'

FIRST_VALUE = 'cat yeah'
SECOND_VALUE = 'echo yeah'


def test_authorized_keys_option_attributes():
    """
    Test attributes of various authorized keys option flags without value
    """
    for testcase in AUTHRORIZED_KEYS_OPTION_FLAGS:
        item = AuthorizedKeyOptionFlag(testcase)
        assert item.option == testcase
        assert isinstance(item.__repr__(), str)


# pylint: disable=comparison-with-itself
def validate_rich_comparisons(a, b):
    """
    Test rich comparisons two options 'a' and 'b' that sort with a before b
    """
    assert a == a
    assert a != b
    assert b != a
    assert a < b
    assert b > a
    assert a <= a
    assert a <= b
    assert b >= a
    assert b >= b

    assert a == str(a)
    assert a != str(b)
    assert a < str(b)
    assert b > str(a)
    assert a <= str(a)
    assert a <= str(b)
    assert b >= str(a)
    assert b >= str(b)


def validate_rich_comparison_errors(a, b):
    """
    Ensure wild comparisons raise TypeError with invalid object unless str() is used
    """
    assert a == str(b)
    with pytest.raises(TypeError):
        assert a == b
    with pytest.raises(TypeError):
        assert a != b
    with pytest.raises(TypeError):
        assert a < b
    with pytest.raises(TypeError):
        assert a > b
    with pytest.raises(TypeError):
        assert a <= b
    with pytest.raises(TypeError):
        assert a >= b


# pylint: disable=too-few-public-methods
class MockInvalidCompareObject:
    """
    Mock class to test comparisons with options

    This class is intentionally missing 'option' and 'value' attributes
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def test_authorized_keys_option_simple_flag_compare_errors():
    """
    Test comparison methods for simple flag fails with invalid object
    """
    a = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[-1])
    b = MockInvalidCompareObject(str(a))
    validate_rich_comparison_errors(a, b)


def test_authorized_keys_option_flag_value_compare_errors():
    """
    Test comparison methods for simple flag fails with invalid object
    """
    a = AuthorizedKeyOptionValue(AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS[0], FIRST_VALUE)
    b = MockInvalidCompareObject(str(a))
    validate_rich_comparison_errors(a, b)


def test_authorized_keys_option_simple_flag_comparisons():
    """
    Test rich comparison functions of the simple option flags
    """
    a = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[0])
    b = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[1])
    validate_rich_comparisons(a, b)


def test_authorized_keys_option_simple_flag_invalid_other():
    """
    Test rich comparison functions of the simple option with invalid object
    """
    a = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[0])
    b = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[1])
    validate_rich_comparisons(a, b)


def test_authorized_keys_option_value_comparisons():
    """
    Test rich comparison functions of the option flags with values

    Test comparison is done by same flag but with different value
    """
    a = AuthorizedKeyOptionValue(AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS[0], FIRST_VALUE)
    b = AuthorizedKeyOptionValue(AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS[0], SECOND_VALUE)
    validate_rich_comparisons(a, b)


def test_authorized_keys_option_comparisons_flag_and_value():
    """
    Test various comparison cases between option flag and option value items

    These never compare the same but should sort by option name
    """
    flag = AuthorizedKeyOptionFlag(AUTHRORIZED_KEYS_OPTION_FLAGS[0])
    option = AuthorizedKeyOptionValue(AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS[0], FIRST_VALUE)
    validate_rich_comparisons(flag, option)


def test_authorized_keys_option_value_attributes():
    """
    Test attributes of various authorized keys option flags with a value
    """
    for testcase in AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS:
        item = AuthorizedKeyOptionValue(testcase, DUMMY_VALUE)
        assert isinstance(item.__repr__(), str)


def test_authorized_keys_option_parser_invalid_simple_flag():
    """
    Test parser for options string with invalid simple flag 'foo'
    """
    with pytest.raises(SSHKeyError):
        parse_option_flag(MOCK_INVALID_SIMPLE_FLAG_NAME)


def test_authorized_keys_option_parser_invalid_flag_value_name():
    """
    Test parser for options string with invalid value flag 'myflag'
    """
    with pytest.raises(SSHKeyError):
        parse_option_flag(MOCK_INVALID_VALUE_FLAG_NAME)


def test_authorized_keys_option_parser_invalid_flag_value_quoting():
    """
    Test parser for options string with valid option flag value using unexpected " quoting
    """
    with pytest.raises(SSHKeyError):
        parse_option_flag(MOCK_INVALID_FLAG_VALUE)
