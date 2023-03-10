#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for 'ssh-assets keys edit' CLI command
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript
from ssh_assets.session import SshAssetSession

from ....conftest import (
    MOCK_BASIC_CONFIG_EXISTING_KEY,
    MOCK_UNKNOWN_KEY_NAME,
)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_no_arguments(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' without any arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_unknown_key_error(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' with unknown key name, causign error
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit', MOCK_UNKNOWN_KEY_NAME]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_argument_confliect(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' with conflicting arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit', '--autoload', '--no-autoload', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_invalid_expire(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' with conflicting arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit', '--expire=never', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_set_autoload(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' with conflicting arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit', '--autoload', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    session = SshAssetSession()
    key_config = session.configuration.keys  # pylint: disable=no-member

    key = key_config.get_key_by_name(MOCK_BASIC_CONFIG_EXISTING_KEY)
    assert key.autoload is True


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_edit_known_key(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys add' with known key to edit
    """
    script = SshAssetsScript()
    testargs = [
        'ssh-assets', 'keys', 'edit', MOCK_BASIC_CONFIG_EXISTING_KEY,
        '--no-autoload',
        '--expire=1d',
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    session = SshAssetSession()
    key_config = session.configuration.keys  # pylint: disable=no-member

    key = key_config.get_key_by_name(MOCK_BASIC_CONFIG_EXISTING_KEY)
    assert key is not None
    assert key.autoload is False
