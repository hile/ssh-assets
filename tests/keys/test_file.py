"""
Unit tests for ssh_assets.keys.file module
"""

import shutil

from pathlib import Path

import pytest

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import MockCalledMethod, MockException, MockRunCommandLineOutput

from ssh_assets.authorized_keys.public_key import PublicKey
from ssh_assets.exceptions import SSHKeyError
from ssh_assets.keys.base import KEY_COMPARE_ATTRIBUTES
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.file import SSHKeyFile

from ..conftest import FILE_NO_PERMISSION, FILE_READONLY


def validate_public_key_processing(obj, tmpdir):
    """
    Validate handling of permission errors reading public key from a file
    """
    prefix = Path(tmpdir, 'public-keys')
    private_key_path = prefix.joinpath(obj.path.name)
    public_key_path = prefix.joinpath(obj.public_key_file_path.name)

    prefix.mkdir(parents=True)
    shutil.copyfile(obj.path, private_key_path)
    shutil.copyfile(obj.public_key_file_path, public_key_path)

    assert private_key_path.is_file()
    assert public_key_path.is_file

    private_key_path.chmod(FILE_READONLY)
    public_key_path.chmod(FILE_NO_PERMISSION)
    private_key = SSHKeyFile(private_key_path)
    with pytest.raises(SSHKeyError):
        private_key.public_key  # pylint: disable=pointless-statement

    # Generate the public key from private key
    public_key_path.unlink()
    private_key.generate_public_key_file()
    assert public_key_path.is_file()

    # Run again, this will not change the file and skips generation
    private_key.generate_public_key_file()
    assert public_key_path.is_file()


def test_keys_file_load(mock_test_key_file, tmpdir):
    """
    Mock loading test keys to the model
    """
    assert mock_test_key_file.is_file()
    obj = SSHKeyFile(mock_test_key_file)
    assert obj.path.is_file()
    assert obj.__key_attributes__ == {}

    for attr in KEY_COMPARE_ATTRIBUTES:
        value = getattr(obj, attr)
        assert isinstance(value, (int, str, KeyHashAlgorithm))

    assert isinstance(obj.__repr__(), str)
    assert obj.__key_attributes__ != {}

    if obj.path.suffix != '.pub':
        assert isinstance(obj.public_key_file_path, Path)
        assert obj.has_public_key_file is True
        assert isinstance(obj.public_key, PublicKey)
        validate_public_key_processing(obj, tmpdir)
    else:
        assert obj.public_key_file_path is None
        assert obj.has_public_key_file is False
        with pytest.raises(SSHKeyError):
            obj.public_key  # pylint: disable=pointless-statement


def test_keys_file_error_generating_public_key(mock_test_key_file, tmpdir):
    """
    Test detecting of errors when generating public key from private key to a path that is existing directory
    """
    filename = Path(tmpdir.strpath, 'permission_denied.txt')
    filename.write_text('\n', encoding='utf-8')
    filename.chmod(FILE_NO_PERMISSION)

    with pytest.raises(SSHKeyError):
        SSHKeyFile(mock_test_key_file).generate_public_key_file(tmpdir.strpath, force=True)

    with pytest.raises(SSHKeyError):
        SSHKeyFile(mock_test_key_file).generate_public_key_file(filename, force=True)


def test_keys_file_load_missing_file(tmpdir):
    """
    Test file loading with missing file
    """
    path = Path(tmpdir.strpath).joinpath('ssh_key_file_missing')
    with pytest.raises(SSHKeyError):
        SSHKeyFile(path).__load_key_attributes__()

    with pytest.raises(SSHKeyError):
        SSHKeyFile(path).generate_public_key_file()
    with pytest.raises(SSHKeyError):
        SSHKeyFile(path).generate_public_key_file()


def test_keys_file_load_empty_output(mock_test_key_file, monkeypatch):
    """
    Test loading SSH key details with empty output from command
    """
    mock_empty_output = MockRunCommandLineOutput(stdout='', stderr='')
    monkeypatch.setattr('ssh_assets.keys.file.run_command_lineoutput', mock_empty_output)
    obj = SSHKeyFile(mock_test_key_file)
    with pytest.raises(SSHKeyError):
        obj.__load_key_attributes__()


def test_keys_file_load_error(mock_test_key_file, monkeypatch):
    """
    Test loading SSH key details with error running command
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.keys.file.run_command_lineoutput', mock_error)
    obj = SSHKeyFile(mock_test_key_file)
    with pytest.raises(SSHKeyError):
        obj.__load_key_attributes__()


def test_keys_file_load_to_agent_call(mock_test_key_file, monkeypatch):
    """
    Test call to load SSH key to agent
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_load)
    SSHKeyFile(mock_test_key_file).load_to_agent()
    assert mock_load.call_count == 1


def test_keys_file_load_to_agent_error(mock_test_key_file, monkeypatch):
    """
    Test call to load SSH key to agent with errors running command
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_error)
    with pytest.raises(SSHKeyError):
        SSHKeyFile(mock_test_key_file).load_to_agent()
    assert mock_error.call_count == 1
