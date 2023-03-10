#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for 'ssh-assets config groups' group subcommand CLI class
"""
from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript


def test_ssh_assets_cli_config_groups_no_args(monkeypatch):
    """
    Test running command 'ssh-assets config groups' with no arguments
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)


def test_ssh_assets_cli_config_groups_help(monkeypatch):
    """
    Test running command 'ssh-assets config groups --help'
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'groups', '--help']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
