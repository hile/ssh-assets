#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for ssh_assets.bin.ssh_assets.groups.edit module
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript

from ....conftest import MOCK_BASIC_CONFIG_EXISTING_GROUP


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_edit_no_arguments(mock_empty_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups edit' with no argumentss
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'edit']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_edit_missing_group(mock_empty_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups edit' with valid group name but no configured
    groups in data
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'edit', MOCK_BASIC_CONFIG_EXISTING_GROUP]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_add_new_group_ok(mock_temporary_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups add' with valid new group arguments
    """
    script = SshAssetsScript()
    testargs = [
        'ssh-assets', 'groups', 'edit', MOCK_BASIC_CONFIG_EXISTING_GROUP,
        '--no-expire',
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
