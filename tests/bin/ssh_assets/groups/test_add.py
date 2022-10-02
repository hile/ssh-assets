"""
Unit tests for ssh_assets.bin.ssh_assets.groups.add module
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript

from ....conftest import MOCK_BASIC_CONFIG_EXISTING_GROUP, MOCK_UNKNOWN_KEY_NAME, TEST_KEYS


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_add_no_arguments(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups add' with no arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'add']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=2)


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_add_expire_conflict(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups add' with conflicting flags for expire
    """
    script = SshAssetsScript()
    testargs = [
        'ssh-assets', 'groups', 'add',
        MOCK_BASIC_CONFIG_EXISTING_GROUP,
        '--expire=1d', '--no-expire'
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_add_existing_group(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups add' with existing group name
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'add', MOCK_BASIC_CONFIG_EXISTING_GROUP]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_add_new_group_ok(mock_temporary_config, monkeypatch):
    """
    Test running command 'ssh-assets config groups add' with valid new group arguments
    """
    script = SshAssetsScript()
    testargs = [
        'ssh-assets', 'groups', 'add', MOCK_UNKNOWN_KEY_NAME,
        '--keys', ','.join(TEST_KEYS),
        '--expire=3d',
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
