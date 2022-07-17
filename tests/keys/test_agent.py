"""
Unit tests for ssh_assets.keys.agent module
"""

import pytest

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import MockCalledMethod, MockException

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.session import SshAssetSession
from ssh_assets.keys.agent import AgentKey

from ..utils import validate_key


# pylint: disable=unused-argument
def test_ssh_agent_keys_attributes(mock_agent_no_keys):
    """
    Test attributes of uninitialized SshAgent object
    """
    session = SshAssetSession()
    assert session.agent.__items__ == []


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_env_var(mock_agent_delete_socket_env):
    """
    Test attributes of SshAgent with environment for ssh-agent not defined
    """
    session = SshAssetSession()
    assert session.agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_socket(mock_agent_dummy_env):
    """
    Test attributes of SshAgent with missing SSH agent socket file
    """
    session = SshAssetSession()
    assert session.agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_dummy_ssh_agent_socket(mock_agent_dummy_socket):
    """
    Test attributes of SshAgent with available SSH agent socket file
    (mock socket, not real agent)
    """
    session = SshAssetSession()
    assert session.agent.is_available is True


# pylint: disable=unused-argument
def test_ssh_agent_keys_load_error(mock_agent_dummy_env):
    """
    Test listing of SSH agent keys with errors running ssh-agent command
    """
    session = SshAssetSession()
    with pytest.raises(SSHKeyError):
        list(session.agent)


def test_ssh_agent_no_loaded_keys(mock_agent_no_keys):
    """
    Test loading SSH agent with standard 'no loaded keys' message in output
    """
    session = SshAssetSession()
    assert len(session.agent) == 0


def test_ssh_agent_keys_list(mock_agent_key_list):
    """
    Test listing of SSH agent keys with mocked key data
    """
    assert isinstance(mock_agent_key_list, list)
    assert len(mock_agent_key_list) > 0
    session = SshAssetSession()
    assert len(session.agent) == len(mock_agent_key_list)

    for key in session.agent:
        validate_key(key, key_class=AgentKey)


def test_ssh_agent_keys_unload_no_agent_socket(mock_basic_config, mock_agent_dummy_env):
    """
    Test error unloading SSH keys from agent when socket is not configured
    """
    with pytest.raises(SSHKeyError):
        SshAssetSession().agent.unload_keys_from_agent(unload_all_keys=True)


def test_ssh_agent_keys_unload_error(mock_basic_config, mock_agent_key_list, monkeypatch):
    """
    Test error unloading SSH keys from agent when the ssh-add command fails
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.is_available', True)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command', mock_error)
    with pytest.raises(SSHKeyError):
        SshAssetSession().agent.unload_keys_from_agent(unload_all_keys=True)


def test_ssh_agent_keys_unload(mock_agent_key_list, monkeypatch):
    """
    Test mocked unloading of SSH agent keys
    """
    mock_command = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.is_available', True)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command', mock_command)
    session = SshAssetSession()
    assert len(session.agent) == len(mock_agent_key_list)

    session.agent.unload_keys_from_agent(unload_all_keys=True)
    assert mock_command.call_count == 1
    args = mock_command.args[0]
    assert args == ('ssh-add', '-D')


def test_ssh_agent_keys_unload_no_keys(mock_basic_config, mock_agent_key_list, monkeypatch):
    """
    Test mocked unloading of SSH agent keys with no listed keys and
    unload_all_keys set to False. The mock function should just return
    """
    mock_command = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.is_available', True)
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_command)
    session = SshAssetSession()
    session.agent.unload_keys_from_agent(keys=[], unload_all_keys=False)
    assert mock_command.call_count == 0


def test_ssh_agent_keys_unload_single_key_not_loaded(mock_basic_config, mock_agent_no_keys, monkeypatch):
    """
    Test mocked unloading of SSH agent keys with no listed keys and
    unload_all_keys set to False. The mock function should just return
    """
    mock_command = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.is_available', True)
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_command)
    session = SshAssetSession()
    session.agent.unload_keys_from_agent(keys=[session.agent.configured_keys[0]], unload_all_keys=False)
    # Unload not called, key was not loaded as defined by mock_agent_no_keys fixture
    assert mock_command.call_count == 0


def test_ssh_agent_keys_unload_single_key_already_loaded(mock_basic_config, mock_agent_key_list, monkeypatch):
    """
    Test mocked unloading of SSH agent keys with no listed keys and
    unload_all_keys set to False. The mock function should just return
    """
    mock_command = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.is_available', True)
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_command)
    session = SshAssetSession()
    session.agent.unload_keys_from_agent(keys=[session.agent.configured_keys[0]], unload_all_keys=False)
    # Unload called normally, key was loaded as defined by mock_agent_key_list fixture
    assert mock_command.call_count == 1
