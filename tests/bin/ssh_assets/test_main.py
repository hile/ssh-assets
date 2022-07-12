"""
Unit tests for ssh-assets main CLI class
"""

import pytest

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import main, SshAssetsScript


def test_ssh_assets_cli_main_no_args():
    """
    Test running command 'ssh-assets' with no arguments
    """
    with pytest.raises(SystemExit):
        main()


def test_ssh_assets_cli_main_help(monkeypatch):
    """
    Test running command 'ssh-assets --help'
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', '--help']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
