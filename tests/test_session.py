#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.session module
"""
from sys_toolkit.tests.mock import MockCalledMethod

from ssh_assets.session import SshAssetSession
from ssh_assets.configuration.keys import SshKeyListConfigurationSection
from ssh_assets.configuration.groups import GroupListConfigurationSection

from .conftest import MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_asset_session_properties(mock_basic_config, mock_agent_key_list):
    """
    Mock basic properties of SSH assets session object
    """
    session = SshAssetSession()
    assert session.configuration.__path__ == mock_basic_config

    # pylint: disable=no-member
    configured_groups = session.configuration.groups
    # pylint: disable=no-member
    configured_keys = session.configuration.keys

    assert isinstance(configured_groups, GroupListConfigurationSection)
    assert isinstance(configured_keys, SshKeyListConfigurationSection)


# pylint: disable=unused-argument
def test_ssh_asset_session_load_configured_keys_all(mock_basic_config, mock_agent_no_keys, monkeypatch):
    """
    Mock calling the load_keys_to_agent method with all keys
    """
    mock_load_to_agent = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.configuration.keys.SshKeyConfiguration.load_to_agent', mock_load_to_agent)
    SshAssetSession().agent.load_keys_to_agent(load_all_keys=True)
    assert mock_load_to_agent.call_count == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_asset_session_load_configured_keys_one_key(mock_basic_config, mock_agent_no_keys, monkeypatch):
    """
    Mock calling the load_keys_to_agent method with no keys
    """
    mock_load_to_agent = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.configuration.keys.SshKeyConfiguration.load_to_agent', mock_load_to_agent)
    session = SshAssetSession()
    # pylint: disable=no-member
    keys = session.configuration.keys[:1]
    session.agent.load_keys_to_agent(keys=keys, load_all_keys=True)
    assert mock_load_to_agent.call_count == 1
