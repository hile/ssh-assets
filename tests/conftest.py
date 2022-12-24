"""
Unit test configuration for ssh_assets module
"""

import os
import shutil
import socket

from pathlib import Path

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import (
    MockRunCommandLineOutput,
    MockException,
)

import pytest

from ssh_assets.keys.constants import SSH_AUTH_SOCK_ENV_VAR, SSH_AGENT_NO_KEYS_MESSAGE

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_BASIC_CONFIG = MOCK_DATA.joinpath('config/basic_config.yml')
MOCK_EMPTY_CONFIG = MOCK_DATA.joinpath('config/empty_config.yml')
MOCK_BASIC_CONFIG_KEYS_COUNT = 4
MOCK_BASIC_CONFIG_AUTOLOAD_KEYS_COUNT = 2
MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT = 3
MOCK_BASIC_CONFIG_GROUP_COUNT = 3

MOCK_BASIC_CONFIG_EXISTING_GROUP = 'demo'
MOCK_BASIC_CONFIG_EXISTING_KEY = 'manual'

MOCK_AGENT_OUTPUT = MOCK_DATA.joinpath('keys/agent.txt')
MOCK_TEST_KEYS = MOCK_DATA.glob('keys/*/ssh_key_*')
MOCK_AGENT_KEY_COUNT = 12

MOCK_UNKNOWN_KEY_NAME = 'nosuchkey'

FILE_READONLY = int('0400', 8)
FILE_NO_PERMISSION = int('0000', 8)
FILE_READWRITE = int('0640', 8)

# List of valid key names to set from basic data
TEST_KEYS = ('manual', 'test')


INVALID_DURATION_VALUES = (
    None,
    '',
    'd20',
    '10y',
    '2d10s3d',
    '0d',
    '-10s',
)
VALID_DURATION_VALUES = (
    '30s',
    '600',
    '2w1d20s',
    600,
)


@pytest.fixture(params=INVALID_DURATION_VALUES)
def invalid_duration_value(request):
    """
    Test fixture to get a list of invalid duration values
    """
    yield request.param


@pytest.fixture(params=VALID_DURATION_VALUES)
def valid_duration_value(request):
    """
    Test fixture to get a list of valid duration values
    """
    yield request.param


@pytest.fixture
def mock_empty_config(monkeypatch):
    """
    Mock empty configuration for SSH assets

    Override loaded default user configuration file with mocked file from MOCK_DATA

    Returns
    -------
    Returns loaded configuration file as pathlib.Path
    """
    monkeypatch.setattr('ssh_assets.session.USER_CONFIGURATION_FILE', MOCK_EMPTY_CONFIG)
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
    monkeypatch.setattr('ssh_assets.session.USER_CONFIGURATION_FILE', MOCK_BASIC_CONFIG)
    return MOCK_BASIC_CONFIG


@pytest.fixture
def mock_temporary_config(monkeypatch, tmpdir):
    """
    Mock basic configuration for SSH assets from temporary directory, used in configuration write tests

    This example configuration contains user configuration file with valid details

    Returns
    -------
    Returns loaded configuration file as pathlib.Path
    """
    filename = Path(tmpdir.strpath, 'assets.yml')
    monkeypatch.setattr('ssh_assets.session.USER_CONFIGURATION_FILE', filename)
    shutil.copyfile(MOCK_BASIC_CONFIG, filename)
    return filename


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
    agent_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    agent_socket.bind(str(mock_agent_dummy_env))
    mock_agent_dummy_env.chmod(FILE_READWRITE)
    return agent_socket


@pytest.fixture
def mock_agent_key_load_error(monkeypatch):
    """
    Mock error loading SSH agent keys
    """
    mock_error = MockException(CommandError)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command_lineoutput', mock_error)


@pytest.fixture
def mock_agent_no_keys(monkeypatch):
    """
    Mock agent with no keys
    """
    lines = [SSH_AGENT_NO_KEYS_MESSAGE]
    mock_keys_list = MockRunCommandLineOutput(stdout=lines)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command_lineoutput', mock_keys_list)
    return lines


@pytest.fixture
def mock_agent_key_list(monkeypatch):
    """
    Mock agent with all mocked test keys loaded to the agent
    """
    lines = MOCK_AGENT_OUTPUT.read_text(encoding='utf-8').splitlines()
    mock_keys_list = MockRunCommandLineOutput(stdout=lines)
    monkeypatch.setattr('ssh_assets.keys.agent.run_command_lineoutput', mock_keys_list)
    return lines
