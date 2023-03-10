#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.token.base module
"""
import pytest

from ssh_assets.token.base import TokenStringValidator, RE_TOKEN

from .conftest import DUMMY_VALUE


def validate_token_string_parser_object(obj, expected_token_count):
    """
    Ensure token parser child class is implemented as expected
    """
    assert isinstance(obj, TokenStringValidator)
    assert isinstance(obj.__suppported_tokens__, tuple)
    if expected_token_count != 0:
        assert len(obj.__suppported_tokens__) == expected_token_count
        # This look goes through all tokens and checks they can be parsed with RE_TOKEN
        for token_type in obj.__suppported_tokens__:
            assert RE_TOKEN.match(token_type.value)
    else:
        assert obj.__suppported_tokens__ == ()


def test_token_string_base_class_properties():
    """
    Test properties of the TokenString base class

    Base class parses no tokens
    """
    validate_token_string_parser_object(TokenStringValidator(), 0)


def test_token_string_base_class_parse_string():
    """
    Test method to parse token strings with the parser base class

    This raises NotImplementedError because the base class defines no tokens to parse
    """
    with pytest.raises(NotImplementedError):
        TokenStringValidator().validate(DUMMY_VALUE)
