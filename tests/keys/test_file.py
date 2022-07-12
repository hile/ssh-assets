"""
Unit tests for ssh_assets.keys.file module
"""

from pathlib import Path

import pytest

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import MockCalledMethod, MockException, MockRunCommandLineOutput

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.keys.base import KEY_COMPARE_ATTRIBUTES
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.file import SSHKeyFile


def test_keys_file_load(mock_test_key_file):
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


def test_keys_file_load_missing_file(tmpdir):
    """
    Test file loading with missing file
    """
    path = Path(tmpdir.strpath).joinpath('ssh_key_file_missing')
    with pytest.raises(SSHKeyError):
        SSHKeyFile(path).__load_key_attributes__()


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
