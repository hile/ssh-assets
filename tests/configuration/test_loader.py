#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.configuration python module
"""
from pathlib import Path

import pytest
import yaml

from sys_toolkit.tests.mock import MockCalledMethod

from ssh_assets.exceptions import SSHAssetsError
from ssh_assets.session import SshAssetSession
from ssh_assets.configuration import SshAssetsConfiguration
from ssh_assets.configuration.groups import GroupConfiguration, GroupListConfigurationSection
from ssh_assets.configuration.keys import SshKeyConfiguration, SshKeyListConfigurationSection
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.agent import SshAgent
from ssh_assets.keys.file import SSHKeyFile

from ..conftest import (
    FILE_READONLY,
    MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT,
    MOCK_BASIC_CONFIG_AUTOLOAD_KEYS_COUNT,
    MOCK_BASIC_CONFIG_GROUP_COUNT,
    MOCK_BASIC_CONFIG_EXISTING_GROUP,
    MOCK_BASIC_CONFIG_KEYS_COUNT,
    MOCK_UNKNOWN_KEY_NAME,
)

EXPECTED_MINUMUM_EXPIRATION_VALUES = {
    'test': '1d',
    'manual': '1h',
    'missing': None,
}


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
    assert len(configured_keys) == MOCK_BASIC_CONFIG_KEYS_COUNT

    assert len(configured_keys.available) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT

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


def test_load_basic_config_key_comparison(mock_basic_config):
    """
    Mock testing key comparison methods
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    a = key_configuration[0]
    b = key_configuration[1]

    assert a == a  # pylint:disable=comparison-with-itself
    assert a == str(a)
    assert a != b
    assert a != str(b)

    assert a <= str(a)
    assert b >= str(b)

    assert a < b
    assert a < str(b)
    assert a <= b
    assert a <= str(b)

    assert b <= b  # pylint:disable=comparison-with-itself
    assert a <= str(b)
    assert b > a
    assert b > str(a)
    assert b >= a
    assert b >= str(a)
    assert b >= b  # pylint:disable=comparison-with-itself
    assert b >= str(b)


def test_load_basic_config_lookup_invalid_name(mock_basic_config):
    """
    Look up keys by invalid name from mock basic configuration
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    assert key_configuration.get_key_by_name(MOCK_UNKNOWN_KEY_NAME) is None


def test_configuration_key_minimum_expire(mock_basic_config):
    """
    Check loading of named keys with expected expiration values in mocked basic config
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    for name, expire_value in EXPECTED_MINUMUM_EXPIRATION_VALUES.items():
        key = key_configuration.get_key_by_name(name)
        assert key.minimum_expire == expire_value


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
    assert len(session.configuration.keys.pending) == MOCK_BASIC_CONFIG_AUTOLOAD_KEYS_COUNT
    session.agent.load_keys_to_agent()
    assert mock_load.call_count == MOCK_BASIC_CONFIG_AUTOLOAD_KEYS_COUNT


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


def test_configuration_add_new_group(mock_temporary_config):
    """
    Test adding new group to configuration
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    group_configuration.configure_group('temporary', keys=[key.name], expire='1h')
    assert mock_temporary_config.is_file()


def test_configuration_update_group_expire(mock_temporary_config):
    """
    Test updating a group in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates group expire field
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    group = group_configuration[0]
    group_configuration.configure_group(group.name, expire='1h')
    assert mock_temporary_config.is_file()

    mock_temporary_config.unlink()
    group_configuration.configure_group(group.name, expire='1h')
    assert not mock_temporary_config.is_file()

    group_configuration.configure_group(group.name, expire=None)
    assert mock_temporary_config.is_file()


def test_configuration_update_group_keys_list_invalid_value(mock_temporary_config):
    """
    Test updating a group in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates group keys field with invalid value (must be a list)
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    group = group_configuration[0]
    with pytest.raises(ValueError):
        group_configuration.configure_group(group.name, keys=key)
    assert not mock_temporary_config.is_file()


def test_configuration_update_group_keys_list_unknown_key(mock_temporary_config):
    """
    Test updating a group in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates group keys field with unknown key
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    group = group_configuration[0]
    with pytest.raises(ValueError):
        group_configuration.configure_group(group.name, keys=['nosuchkey'])
    assert not mock_temporary_config.is_file()


def test_configuration_update_group_keys_list_valid(mock_temporary_config):
    """
    Test updating a group in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates group keys field with valid keys
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    key = key_configuration[0]

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    group = group_configuration[0]
    group_configuration.configure_group(group.name, keys=[key.name])
    assert mock_temporary_config.is_file()

    mock_temporary_config.unlink()
    group_configuration.configure_group(group.name, keys=[key.name])
    assert not mock_temporary_config.is_file()


def test_configuration_keys_delitem_unknown_key(mock_temporary_config):
    """
    Test __delitem__ method with unknown key name
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    assert len(key_configuration) == MOCK_BASIC_CONFIG_KEYS_COUNT
    del key_configuration[MOCK_UNKNOWN_KEY_NAME]
    assert len(key_configuration) == MOCK_BASIC_CONFIG_KEYS_COUNT


def test_configuration_groups_delitem_unknown_key(mock_temporary_config):
    """
    Test __delitem__ method with unknown group name
    """
    session = SshAssetSession()
    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    assert len(group_configuration) == MOCK_BASIC_CONFIG_GROUP_COUNT
    del group_configuration[MOCK_UNKNOWN_KEY_NAME]
    assert len(group_configuration) == MOCK_BASIC_CONFIG_GROUP_COUNT


def test_configuration_groups_delete_group(mock_temporary_config):
    """
    Test deleting a group from configuration
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    group_configuration = session.configuration.groups
    deleted_group = group_configuration.get_group_by_name(MOCK_BASIC_CONFIG_EXISTING_GROUP)

    print('delete', deleted_group)
    group_count = len(group_configuration)
    group_configuration.delete_group(deleted_group.name)
    assert group_count == len(group_configuration) + 1
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    group_count = len(group_configuration)
    group_configuration.delete_group(deleted_group.name)
    # No changes, configuration is not saved
    assert not mock_temporary_config.is_file()


def test_configuration_delete_key(mock_temporary_config):
    """
    Test deleting a key from configuration
    """
    session = SshAssetSession()
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    # pylint: disable=no-member
    key_configuration = session.configuration.keys
    deleted_key = key_configuration[0]

    key_count = len(key_configuration)
    key_configuration.delete_key(deleted_key.name)
    assert key_count == len(key_configuration) + 1
    assert mock_temporary_config.is_file()
    mock_temporary_config.unlink()

    key_count = len(key_configuration)
    key_configuration.delete_key(deleted_key.name)
    # No changes, configuration is not saved
    assert not mock_temporary_config.is_file()


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
    that can be deleted. This test case updates key path
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


def test_configuration_update_key_expire(mock_temporary_config):
    """
    Test updating a key in SSH assets configuration with the temporary configuration file
    that can be deleted. This test case updates 'expire' value
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


def test_configuration_update_key_autoload(mock_temporary_config):
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
