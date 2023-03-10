#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.token.server module
"""
import pytest

from .conftest import DUMMY_VALUE
from .test_base import validate_token_string_parser_object

UNEXPECTED_VALID_TOKEN_STRING = 'test-%u-server-hash-%C'


def test_token_server_token_class_loader_attributes(server_token_loader):
    """
    Test the server token loader classes define required parameters
    """
    validate_token_string_parser_object(
        server_token_loader(),
        len(server_token_loader.__suppported_tokens__)
    )


def test_token_server_token_no_tokens(server_token_loader):
    """
    Test loading server token loader with a string with no tokens
    """
    tokens = server_token_loader().validate(DUMMY_VALUE)
    assert not tokens


def test_token_server_token_invalid_token(server_token_loader):
    """
    Test loading server token loader with a string containing invalid token (from server config)
    """
    with pytest.raises(ValueError):
        server_token_loader().validate(UNEXPECTED_VALID_TOKEN_STRING)


def test_token_server_token_valid_token(server_token_loader):
    """
    Test loading server token loader with a string containing valid token
    """
    validator = server_token_loader()
    token_string = f'test-{validator.expected_tokens[0]}-case_{validator.expected_tokens[1]}.example'
    tokens = validator.validate(token_string)
    assert tokens == validator.expected_tokens[:2]
