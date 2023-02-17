"""
Unit tests for ssh_assets.configuration.keys module
"""
from pathlib import Path

import pytest

from sys_toolkit.tests.mock import MockCalledMethod

from ssh_assets.authorized_keys import AuthorizedKeys
from ssh_assets.authorized_keys.constants import DEFAULT_AUTHORIZED_KEYS_FILE
from ssh_assets.keys.constants import SshKeyType
from ssh_assets.exceptions import SSHKeyError
from ssh_assets.session import SshAssetSession


# pylint: disable=unused-argument
def test_keys_identity_parameters(
        mock_basic_config,
        mock_agent_key_list,
        mock_test_key_file,
        monkeypatch) -> None:
    """
    Test getting the identity parameters of keys loaded to the agent
    """
    session = SshAssetSession()
    for key in session.configuration.keys.available:
        identity_parameters = key.identity_parameters
        # Name and key type are added to defaults
        assert len(identity_parameters) > 0
        for attr in identity_parameters:
            print(key, attr)
            assert isinstance(attr, str)


# pylint: disable=unused-argument
def test_keys_file_load_available_all_keys_to_agent(
        mock_basic_config,
        mock_agent_key_list,
        mock_test_key_file,
        monkeypatch) -> None:
    """
    Test call to load SSH keys to agent, with autoload marked for available keys only
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_load)
    session = SshAssetSession()

    assert len(session.configuration.keys.pending) == 0
    session.agent.load_keys_to_agent()
    assert mock_load.call_count == 0

    assert isinstance(session.user_authorized_keys, AuthorizedKeys)
    assert session.user_authorized_keys.path == Path(DEFAULT_AUTHORIZED_KEYS_FILE).expanduser()


# pylint: disable=unused-argument
def test_keys_configured_load_to_agent(mock_basic_config, mock_agent_no_keys, monkeypatch) -> None:
    """
    Load configured test key to agent
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.load_to_agent', mock_load)
    session = SshAssetSession()

    key = session.configuration.keys[0]
    assert key.available is True
    assert key.loaded is False
    assert mock_load.call_count == 0
    key.load_to_agent()
    assert mock_load.call_count == 1


# pylint: disable=unused-argument
def test_keys_configured_unload_from_agent(mock_basic_config, mock_agent_key_list, monkeypatch) -> None:
    """
    Load configured test key to agent
    """
    mock_unload = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.unload_from_agent', mock_unload)
    session = SshAssetSession()

    key = session.configuration.keys[0]
    assert key.available is True
    assert key.loaded is True
    assert mock_unload.call_count == 0
    key.unload_from_agent()
    assert mock_unload.call_count == 1


# pylint: disable=unused-argument
def test_keys_available_key_type(mock_basic_config, mock_agent_key_list, monkeypatch) -> None:
    """
    Test looking up key type for unavailable key
    """
    key = SshAssetSession().key_filter_set.filter_available(available=True).keys[0]
    assert isinstance(key.key_type, SshKeyType)


# pylint: disable=unused-argument
def test_keys_unavailable_key_type(mock_basic_config, mock_agent_key_list, monkeypatch) -> None:
    """
    Test looking up key type for unavailable key
    """
    key = SshAssetSession().key_filter_set.filter_available(available=False).keys[0]
    assert key.key_type is None


# pylint: disable=unused-argument
def test_keys_unavailable_load_to_agent(mock_basic_config, mock_agent_key_list, monkeypatch) -> None:
    """
    Load unavailable test key to agent
    """
    mock_unload = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.load_to_agent', mock_unload)
    key = SshAssetSession().key_filter_set.filter_available(available=False).keys[0]
    with pytest.raises(SSHKeyError):
        key.load_to_agent()


# pylint: disable=unused-argument
def test_keys_unavailable_unload_from_agent(mock_basic_config, mock_agent_key_list, monkeypatch) -> None:
    """
    Unload unavailable test key from agent
    """
    mock_unload = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.unload_from_agent', mock_unload)
    key = SshAssetSession().key_filter_set.filter_available(available=False).keys[0]
    with pytest.raises(SSHKeyError):
        key.unload_from_agent()
