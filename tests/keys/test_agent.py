"""
Unit tests for ssh_assets.keys.agent module
"""

import pytest

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.keys.agent import SshAgentKeys, AgentKey

from ..utils import validate_key


def test_ssh_agent_keys_attributes():
    """
    Test attributes of uninitialized SshAgentKeys object
    """
    agent = SshAgentKeys()
    assert agent.__items__ == []


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_env_var(mock_agent_delete_socket_env):
    """
    Test attributes of SshAgentKeys with environment for ssh-agent not defined
    """
    agent = SshAgentKeys()
    assert agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_missing_ssh_agent_socket(mock_agent_dummy_env):
    """
    Test attributes of SshAgentKeys with missing SSH agent socket file
    """
    agent = SshAgentKeys()
    assert agent.is_available is False


# pylint: disable=unused-argument
def test_ssh_agent_dummy_ssh_agent_socket(mock_agent_dummy_socket):
    """
    Test attributes of SshAgentKeys with available SSH agent socket file
    (mock socket, not real agent)
    """
    agent = SshAgentKeys()
    assert agent.is_available is True


# pylint: disable=unused-argument
def test_ssh_agent_keys_load_error(mock_agent_dummy_env):
    """
    Test listing of SSH agent keys with errors running ssh-agent command
    """
    agent = SshAgentKeys()
    with pytest.raises(SSHKeyError):
        list(agent)


def test_ssh_agent_keys_list(mock_agent_key_list):
    """
    Test listing of SSH agent keys with mocked key data
    """
    assert isinstance(mock_agent_key_list, list)
    assert len(mock_agent_key_list) > 0
    agent = SshAgentKeys()
    assert len(agent) == len(mock_agent_key_list)

    for key in agent:
        validate_key(key, key_class=AgentKey)
