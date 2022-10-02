"""
Unit tests for 'ssh-assets keys add' CLI command
"""
from pathlib import Path

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript
from ssh_assets.session import SshAssetSession

from ....conftest import MOCK_BASIC_CONFIG_EXISTING_KEY, MOCK_UNKNOWN_KEY_NAME

TEST_KEY_PATH = '/tmp/test-key'


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_add_no_arguments(mock_temporary_config, monkeypatch):
    """
    Test running 'ssh-assets keys add' without any arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'add']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_add_existing_key_error(mock_temporary_config, monkeypatch):
    """
    Test running 'ssh-assets keys add' with existing key name, causign error
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'add', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_add_invalid_expire(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys add' with confilicting arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'edit', '--expire=never', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_add_argument_conflict(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys add' with confilicting arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'add', '--autoload', '--no-autoload', MOCK_BASIC_CONFIG_EXISTING_KEY]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_add_key_all_arguments_ok(mock_temporary_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys add' with name key and all arguments
    """
    script = SshAssetsScript()
    testargs = [
        'ssh-assets', 'keys', 'add', MOCK_UNKNOWN_KEY_NAME,
        '--path', TEST_KEY_PATH,
        '--autoload',
        '--expire=1d',
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    session = SshAssetSession()
    key_config = session.configuration.keys  # pylint: disable=no-member

    key = key_config.get_key_by_name(MOCK_UNKNOWN_KEY_NAME)
    assert key is not None
    assert key.path == Path(TEST_KEY_PATH).resolve()
    assert key.autoload is True
