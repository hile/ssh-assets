#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.token.client module
"""
import pytest

from .conftest import DUMMY_VALUE
from .test_base import validate_token_string_parser_object

UNEXPECTED_VALID_TOKEN_STRING = 'test-%u-domain%D'


def test_token_client_token_class_loader_attributes(client_token_loader):
    """
    Test the client token loader classes define required parameters
    """
    validate_token_string_parser_object(
        client_token_loader(),
        len(client_token_loader.__suppported_tokens__)
    )


def test_token_client_token_no_tokens(client_token_loader):
    """
    Test loading client token loader with a string with no tokens
    """
    tokens = client_token_loader().validate(DUMMY_VALUE)
    assert not tokens


def test_token_client_token_invalid_token(client_token_loader):
    """
    Test loading client token loader with a string containing invalid token (from server config)
    """
    with pytest.raises(ValueError):
        client_token_loader().validate(UNEXPECTED_VALID_TOKEN_STRING)
