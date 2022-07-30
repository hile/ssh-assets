"""
Unit tests for 'ssh-assets config' group subcommand CLI class
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript


def test_ssh_assets_cli_config_no_args(monkeypatch):
    """
    Test running command 'ssh-assets config' with no arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'config']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_ssh_assets_cli_config_help(monkeypatch):
    """
    Test running command 'ssh-assets config --help'
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'config', '--help']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
