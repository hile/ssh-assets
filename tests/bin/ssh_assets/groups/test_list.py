"""
Unit tests for ssh_assets.bin.ssh_assets.groups.list module
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript

BASIC_CONFIG_GROUPS_COUNT = 3


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_list_empty_config(mock_empty_config, monkeypatch, capsys):
    """
    Test running command 'ssh-assets config groups list' with empty configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 0


# pylint: disable=unused-argument
def test_ssh_assets_cli_config_groups_list_basic_config(mock_basic_config, monkeypatch, capsys):
    """
    Test running command 'ssh-assets config groups list' with empty configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == BASIC_CONFIG_GROUPS_COUNT
