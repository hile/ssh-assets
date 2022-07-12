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
    Test attributes of uninitialized SshAgentKeys object
    """
    session = SshAssetSession()
    assert session.agent.__items__ == []


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_env_var(mock_agent_delete_socket_env):
    """
    Test attributes of SshAgentKeys with environment for ssh-agent not defined
    """
    session = SshAssetSession()
    assert session.agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_socket(mock_agent_dummy_env):
    """
    Test attributes of SshAgentKeys with missing SSH agent socket file
    """
    session = SshAssetSession()
    assert session.agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_dummy_ssh_agent_socket(mock_agent_dummy_socket):
    """
    Test attributes of SshAgentKeys with available SSH agent socket file
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


def test_ssh_agent_keys_unload_no_agent_socket(mock_agent_dummy_env):
    """
    Test error unloading SSH keys from agent when socket is not configured
    """
    with pytest.raises(SSHKeyError):
        SshAssetSession().unload_keys()


def test_ssh_agent_keys_unload_error(mock_agent_key_list, monkeypatch):
    """
    Test error unloading SSH keys from agent when the ssh-add command fails
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.session.run_command', mock_error)
    with pytest.raises(SSHKeyError):
        SshAssetSession().unload_keys()


def test_ssh_agent_keys_unload(mock_agent_key_list, monkeypatch):
    """
    Test mocked unloading of SSH agent keys
    """
    mock_command = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.session.run_command', mock_command)
    assert isinstance(mock_agent_key_list, list)
    assert len(mock_agent_key_list) > 0
    session = SshAssetSession()
    assert len(session.agent) == len(mock_agent_key_list)

    session.unload_keys()
    assert mock_command.call_count == 1
    args = mock_command.args[0]
    assert args == ('ssh-add', '-D')
