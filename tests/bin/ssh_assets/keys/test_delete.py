"""
Unit tests for 'ssh-assets keys delete' CLI command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript
from ssh_assets.session import SshAssetSession

from ....conftest import (
    MOCK_BASIC_CONFIG_EXISTING_KEY,
    MOCK_UNKNOWN_KEY_NAME,
)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_delete_no_arguments(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys edit' without any arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'delete']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_delete_unknown_key_error(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys delete' with unknown key name, causign error
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'delete', MOCK_UNKNOWN_KEY_NAME]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_delete_known_key(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys delete' with known key to delete
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'delete', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    session = SshAssetSession()
    key_config = session.configuration.keys  # pylint: disable=no-member
    key = key_config.get_key_by_name(MOCK_BASIC_CONFIG_EXISTING_KEY)
    assert key is None
