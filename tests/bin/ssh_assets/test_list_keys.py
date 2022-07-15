"""
Unit tests for 'ssh-assets list-keys' CLI command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript

from ...conftest import MOCK_BASIC_CONFIG_KEYS_COUNT

KEY_NO_MATCH = 'nomatch'

KEY_MATCH_TEST = 'tests/mock/keys/RFC4716/ssh_key_dsa'
KEY_MATCH_MISSING = 'miss*'


# pylint: disable=unused-argument
def test_ssh_assets_list_keys_no_keys(mock_empty_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets list-keys' without any arguments

    This will return with code 1 because there are no keys in mocked empty config
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'list-keys']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


# pylint: disable=unused-argument
def test_ssh_assets_list_keys_mock_keys(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets list-keys' without any arguments using mocked basic configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'list-keys']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == MOCK_BASIC_CONFIG_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_assets_list_keys_no_match(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets list-keys' with key parameters that do not match any keys
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'list-keys', KEY_NO_MATCH]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


# pylint: disable=unused-argument
def test_ssh_assets_list_keys_existing(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets list-keys' with key parameters that match configured keys
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'list-keys', KEY_MATCH_TEST, KEY_MATCH_MISSING]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 2
