"""
Unit test configuration for ssh_assets module
"""

import os
import socket

from pathlib import Path

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import (
    MockRunCommandLineOutput,
    MockException,
)

import pytest

from ssh_assets.keys.constants import SSH_AUTH_SOCK_ENV_VAR

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_BASIC_CONFIG = MOCK_DATA.joinpath('config/basic_config.yml')
MOCK_EMPTY_CONFIG = MOCK_DATA.joinpath('config/empty_config.yml')

MOCK_AGENT_OUTPUT = MOCK_DATA.joinpath('keys/agent.txt')
MOCK_TEST_KEYS = MOCK_DATA.glob('keys/*/ssh_key_*')

PERM_READWRITE = int('0640', 8)


@pytest.fixture
def mock_empty_config(monkeypatch):
    """
    Mock empty configuration for SSH assets

    Override loaded default user configuration file with mocked file from MOCK_DATA

    Returns
    -------
    Returns loaded configuration file as pathlib.Path
    """
    monkeypatch.setattr('ssh_assets.configuration.USER_CONFIGURATION_FILE', MOCK_EMPTY_CONFIG)
    return MOCK_EMPTY_CONFIG


@pytest.fixture
def mock_basic_config(monkeypatch):
    """
    Mock basic configuration for SSH assets

    This example configuration contains user configuration file with valid details

    Returns
    -------
    Returns loaded configuration file as pathlib.Path
    """
    monkeypatch.setattr('ssh_assets.configuration.USER_CONFIGURATION_FILE', MOCK_BASIC_CONFIG)
    return MOCK_BASIC_CONFIG


@pytest.fixture(params=MOCK_TEST_KEYS)
def mock_test_key_file(request):
    """
    Mock loading of the mocked test SSH keys to the test case
    """
    path = request.param
    print(f'test key {path}')
    yield path


@pytest.fixture
def mock_agent_delete_socket_env(monkeypatch):
    """
    Mock a dummy SSH agent socket environment
    """
    if os.environ.get(SSH_AUTH_SOCK_ENV_VAR, None):
        monkeypatch.delenv(SSH_AUTH_SOCK_ENV_VAR)


# pylint: disable=redefined-outer-name, unused-argument
@pytest.fixture
def mock_agent_dummy_env(mock_agent_delete_socket_env, monkeypatch, tmpdir):
    """
    Mock a dummy SSH agent socket environment variable without creating the socket file
    """
    path = Path(tmpdir.strpath).joinpath('ssh-agent.sock')
    monkeypatch.setenv(SSH_AUTH_SOCK_ENV_VAR, str(path))
    yield path


# pylint: disable=redefined-outer-name
@pytest.fixture
def mock_agent_dummy_socket(mock_agent_dummy_env):
    """
    Mock a dummy SSH agent socket environment variable with creating a dummy SSH agent
    socket (nothing really listening to it)
    """
    print(mock_agent_dummy_env)
    agent_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    agent_socket.bind(str(mock_agent_dummy_env))
    mock_agent_dummy_env.chmod(PERM_READWRITE)
    return agent_socket


@pytest.fixture
def mock_agent_key_load_error(monkeypatch):
    """
    Mock error loading SSH agent keys
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command_lineoutput', mock_error)


@pytest.fixture
def mock_agent_key_list(monkeypatch):
    """
    Mock agent with all mocked test keys loaded to the agent
    """
    lines = MOCK_AGENT_OUTPUT.read_text(encoding='utf-8').splitlines()
    mock_keys_list = MockRunCommandLineOutput(stdout=lines)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command_lineoutput', mock_keys_list)
    return lines
