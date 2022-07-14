"""
Test authorized keys file loader
"""

import shutil

from pathlib import Path

import pytest

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.authorized_keys import AuthorizedKeys
from ssh_assets.authorized_keys.loader import AuthorizedKeyEntry
from ssh_assets.authorized_keys.options import AuthorizedKeyOptionFlag

from ..conftest import MOCK_DATA

VALID_AUTHORIZED_KEYS_FILE = MOCK_DATA.joinpath('authorized_keys/valid.txt')
EXPECTED_KEYS_COUNT = 8

INVALID_ENTRY = 'AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4/WBdHPxuALr1iYzUT21 info@example.net'
INVALID_FORMAT_ENTRY = 'AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4 ssh-rsa'
VALID_ENTRY = 'pty ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4/WBdHPxuALr1iYzUT21 info@example.net'


def test_authorized_keys_parser_invalid_missing_key_type():
    """
    Test parser for trivial, invalid entry in SSH keys: missing key type
    """
    with pytest.raises(SSHKeyError):
        AuthorizedKeyEntry(INVALID_ENTRY)


def test_authorized_keys_parser_invalid_missing_base64_hash():
    """
    Test parser for trivial, invalid entry in SSH keys: missing base64 hash after key type
    """
    with pytest.raises(SSHKeyError):
        AuthorizedKeyEntry(INVALID_FORMAT_ENTRY)


def test_authorized_keys_parser_valid_entry():
    """
    Test parser for trivial, valid entry in SSH keys data
    """
    entry = AuthorizedKeyEntry(VALID_ENTRY)
    assert entry.options == [AuthorizedKeyOptionFlag('pty')]


def test_authorized_keys_loader_valid_file():
    """
    Test loading a valid authorized keys file from mocked data
    """
    obj = AuthorizedKeys(VALID_AUTHORIZED_KEYS_FILE)
    assert len(obj) == EXPECTED_KEYS_COUNT
    for item in obj:
        assert isinstance(item.__repr__(), str)


def test_authorized_keys_loader_missing_file(tmpdir):
    """
    Test loading authorized keys file with missing file path
    """
    path = Path(tmpdir.strpath, 'missing_key_file')
    obj = AuthorizedKeys(path)
    with pytest.raises(SSHKeyError):
        obj.update()


def test_authorized_keys_loader_file_load_error(tmpdir):
    """
    Test loading authorized keys with OSError from reading the file (no permissions to the file)
    """
    path = Path(tmpdir.strpath, 'missing_key_file')
    shutil.copyfile(VALID_AUTHORIZED_KEYS_FILE, path)
    path.chmod(int('0000', 8))

    obj = AuthorizedKeys(path)
    with pytest.raises(SSHKeyError):
        obj.update()
