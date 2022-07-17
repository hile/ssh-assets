"""
Unit tests for ssh_assets.configuration python module
"""
from pathlib import Path

import pytest
import yaml

from sys_toolkit.tests.mock import MockCalledMethod

from ssh_assets.exceptions import SSHAssetsError
from ssh_assets.session import SshAssetSession
from ssh_assets.authorized_keys import AuthorizedKeys
from ssh_assets.authorized_keys.constants import DEFAULT_AUTHORIZED_KEYS_FILE
from ssh_assets.configuration import SshAssetsConfiguration
from ssh_assets.configuration.groups import GroupConfiguration, GroupListConfigurationSection
from ssh_assets.configuration.keys import SshKeyConfiguration, SshKeyListConfigurationSection
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.agent import SshAgent
from ssh_assets.keys.file import SSHKeyFile

from .conftest import FILE_READONLY


MOCK_UNKNOWN_KEY_NAME = 'nosuchkey'

EXPECTED_KEY_COUNT = 3
EXPECTED_AVAILABLE_KEY_COUNT = 2
EXPECTED_AUTOLOAD_KEY_COUNT = 1


def validate_configuration_dictionary(data):
    """
    Validate sanity of a configuration dictionary result
    """
    for attr in ('groups', 'keys'):
        assert attr in data
        assert isinstance(data[attr], list)
        assert data[attr] != []


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
    configured_groups = session.configuration.groups
    # pylint: disable=no-member
    configured_keys = session.configuration.keys
    assert len(configured_keys) == EXPECTED_KEY_COUNT

    assert len(configured_keys.available) == EXPECTED_AVAILABLE_KEY_COUNT

    for item in configured_groups:
        assert isinstance(item, GroupConfiguration)
        assert isinstance(item.__repr__(), str)
        assert isinstance(item.name, str)
        assert isinstance(item.__key_configuration__, SshKeyListConfigurationSection)
        assert isinstance(item.private_keys, list)
        assert isinstance(item.as_dict(), dict)

    for item in configured_keys:
        assert isinstance(item, SshKeyConfiguration)
        assert isinstance(item.__repr__(), str)
        assert isinstance(item.private_key, SSHKeyFile)
        assert isinstance(item.hash_algorithm, KeyHashAlgorithm)
        assert isinstance(item.__agent__, SshAgent)
        assert isinstance(item.__group_configuration__, GroupListConfigurationSection)
        assert isinstance(item.groups, list)
        assert isinstance(item.as_dict(), dict)

        if item.available:
            assert isinstance(item.hash, str)
            assert item.loaded is True
        else:
            assert item.hash is None
            assert item.loaded is False


def test_load_basic_config_as_dict(mock_basic_config, mock_agent_key_list):
    """
    Minimal validation for basic configuration mock file contents from as_dict()
    """
    session = SshAssetSession()
    data = session.configuration.as_dict()
    assert isinstance(data, dict)
    validate_configuration_dictionary(data)


def test_load_basic_config_as_yaml(mock_basic_config, mock_agent_key_list):
    """
    Minimal validation for basic configuration mock file contents from as_yaml()
    """
    session = SshAssetSession()
    output = session.configuration.as_yaml()
    assert isinstance(output, str)
    data = yaml.safe_load(output)
    validate_configuration_dictionary(data)


def test_load_basic_config_lookup_existing(mock_basic_config):
    """
    Look up keys by name from mock basic configuration
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    for key in key_configuration:
        item = key_configuration.get_key_by_name(key.name)
        assert item == key


def test_load_basic_config_lookup_invalid_name(mock_basic_config):
    """
    Look up keys by invalid name from mock basic configuration
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    assert key_configuration.get_key_by_name(MOCK_UNKNOWN_KEY_NAME) is None


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
    session.agent.load_keys_to_agent()
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
    session.agent.load_keys_to_agent()
    assert mock_load.call_count == 0

    assert isinstance(session.user_authorized_keys, AuthorizedKeys)
    assert session.user_authorized_keys.path == Path(DEFAULT_AUTHORIZED_KEYS_FILE).expanduser()


# pylint: disable=unused-argument
def test_keys_configured_load_to_agent(mock_basic_config, mock_agent_no_keys, monkeypatch):
    """
    Load configured test key to agent
    """
    mock_load = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.load_to_agent', mock_load)
    session = SshAssetSession()

    # pylint: disable=no-member
    key = session.configuration.keys[0]
    assert key.available is True
    assert key.loaded is False
    assert mock_load.call_count == 0
    key.load_to_agent()
    assert mock_load.call_count == 1


# pylint: disable=unused-argument
def test_keys_configured_unload_from_agent(mock_basic_config, mock_agent_key_list, monkeypatch):
    """
    Load configured test key to agent
    """
    mock_unload = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.file.SSHKeyFile.unload_from_agent', mock_unload)
    session = SshAssetSession()

    # pylint: disable=no-member
    key = session.configuration.keys[0]
    assert key.available is True
    assert key.loaded is True
    assert mock_unload.call_count == 0
    key.unload_from_agent()
    assert mock_unload.call_count == 1


def test_configuration_save_default_file(mock_temporary_config):
    """
    Test saving configuration to default file using temporary file
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()
    session.configuration.save()
    assert mock_temporary_config.is_file()


def test_configuration_save_error(mock_temporary_config):
    """
    Test errors saving configuration to default file using temporary file
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.chmod(FILE_READONLY)
    with pytest.raises(SSHAssetsError):
        session.configuration.save()


def test_configuration_save_different_filename(mock_temporary_config):
    """
    Test saving configuration to a different file given as string
    """
    testfile = Path(f'{mock_temporary_config}.tmp.yml')
    session = SshAssetSession()
    assert not testfile.is_file()
    session.configuration.save(str(testfile))
    assert testfile.is_file()


def test_configuration_add_new_key(mock_temporary_config, tmpdir):
    """
    Test adding new key to configuration
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key_configuration.configure_key('temporary', path=tmpdir.strpath)
    assert mock_temporary_config.is_file()


def test_configuration_update_key_path(mock_temporary_config, tmpdir):
    """
    Test updating a key in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case key path
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    key_configuration.configure_key(key.name, path=tmpdir.strpath)
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    key_configuration.configure_key(key.name, path=tmpdir.strpath)
    assert not mock_temporary_config.is_file()


def test_configuration_update_key_expire(mock_temporary_config, tmpdir):
    """
    Test updating a key in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case expiration
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    key_configuration.configure_key(key.name, expire='1d')
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    key_configuration.configure_key(key.name, expire='1d')
    assert not mock_temporary_config.is_file()

    key_configuration.configure_key(key.name, expire=None)
    assert mock_temporary_config.is_file()


def test_configuration_update_key_autoload(mock_temporary_config, tmpdir):
    """
    Test updating a key in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates autoload field
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    key_configuration.configure_key(key.name, autoload=False)
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    key_configuration.configure_key(key.name, autoload=False)
    assert not mock_temporary_config.is_file()

    key_configuration.configure_key(key.name, autoload=None)
    assert mock_temporary_config.is_file()
