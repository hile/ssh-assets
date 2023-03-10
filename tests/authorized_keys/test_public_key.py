#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.authorized_keys.public_key module
"""
import pytest

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.authorized_keys.options import AuthorizedKeyOptionFlag
from ssh_assets.authorized_keys.public_key import PublicKey

from .constants import (
    INVALID_ENTRY,
    INVALID_FORMAT_ENTRY,
    INVALID_BASE64_ENTRY,
    VALID_ENTRY,
)


def test_authorized_keys_parser_invalid_missing_key_type():
    """
    Test parser for trivial, invalid entry in SSH keys: missing key type
    """
    with pytest.raises(SSHKeyError):
        PublicKey(INVALID_ENTRY)


def test_authorized_keys_parser_missing_base64_hash():
    """
    Test parser for trivial, invalid entry in SSH keys: missing base64 hash after key type
    """
    with pytest.raises(SSHKeyError):
        PublicKey(INVALID_FORMAT_ENTRY)


def test_authorized_keys_parser_invalid_base64_hash():
    """
    Test parser for trivial, invalid entry in SSH keys: base64 hash value is invalid
    """
    with pytest.raises(SSHKeyError):
        PublicKey(INVALID_BASE64_ENTRY)


def test_authorized_keys_parser_valid_entry():
    """
    Test parser for trivial, valid entry in SSH keys data
    """
    entry = PublicKey(VALID_ENTRY)
    assert entry.options == [AuthorizedKeyOptionFlag('pty')]
