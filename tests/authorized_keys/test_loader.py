"""
Test authorized keys file loader
"""

import shutil

from pathlib import Path

import pytest

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.authorized_keys import AuthorizedKeys

from .constants import (
    VALID_AUTHORIZED_KEYS_FILE,
    EXPECTED_KEYS_COUNT,
)


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
