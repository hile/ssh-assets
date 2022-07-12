"""
Unit tests for ssh_assets.configuration python module
"""

from sys_toolkit.tests.mock import MockCalledMethod

from ssh_assets.session import SshAssetSession
from ssh_assets.configuration import SshAssetsConfiguration, SshKeyConfiguration
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.agent import SshAgentKeys
from ssh_assets.keys.file import SSHKeyFile

EXPECTED_KEY_COUNT = 3
EXPECTED_AVAILABLE_KEY_COUNT = 2
EXPECTED_AUTOLOAD_KEY_COUNT = 1


def test_load_empty_config(mock_empty_config):
    """
    Test loading empty configuration from mocked empty configuration file
    """
    session = SshAssetSession()
    assert isinstance(session.configuration, SshAssetsConfiguration)
    assert session.configuration.__path__ == mock_empty_config
    assert session.configuration.__path__.exists()


# pylint: disable=unused-argument
def test_load_basic_config(mock_basic_config, mock_agent_key_list):
    """
    Test loading basic SSH assets configuration file with basic key details
    """
    session = SshAssetSession()
    assert session.configuration.__path__ == mock_basic_config

    # pylint: disable=no-member
    configured_keys = session.configuration.keys
    assert len(configured_keys) == EXPECTED_KEY_COUNT

    for key in configured_keys.available:
        print(key.path)
    assert len(configured_keys.available) == EXPECTED_AVAILABLE_KEY_COUNT

    for item in configured_keys:
        assert isinstance(item, SshKeyConfiguration)
        assert isinstance(item.__repr__(), str)
        assert isinstance(item.key, SSHKeyFile)
        assert isinstance(item.hash_algorithm, KeyHashAlgorithm)
        assert isinstance(item.__agent__, SshAgentKeys)

        if item.available:
            assert isinstance(item.hash, str)
            assert item.loaded is True
        else:
            assert item.hash is None
            assert item.loaded is False


def test_keys_file_load_available_autoload_keys_to_agent(
        mock_basic_config,
        mock_agent_no_keys,
        mock_test_key_file,
        monkeypatch):
    """
    Test call to load SSH keys to agent, with autoload marked for available keys only
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_load)
    session = SshAssetSession()

    # pylint: disable=no-member
    assert len(session.configuration.keys.pending) == EXPECTED_AUTOLOAD_KEY_COUNT
    session.load_available_keys()
    assert mock_load.call_count == EXPECTED_AUTOLOAD_KEY_COUNT


def test_keys_file_load_available_all_keys_to_agent(
        mock_basic_config,
        mock_agent_key_list,
        mock_test_key_file,
        monkeypatch):
    """
    Test call to load SSH keys to agent, with autoload marked for available keys only
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.run_command', mock_load)
    session = SshAssetSession()

    # pylint: disable=no-member
    assert len(session.configuration.keys.pending) == 0
    session.load_available_keys()
    assert mock_load.call_count == 0
