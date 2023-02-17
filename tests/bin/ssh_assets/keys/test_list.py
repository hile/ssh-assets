"""
Unit tests for 'ssh-assets keys list' CLI command
"""

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript
from ssh_assets.constants import NO_KEYS_CONFIGURED

from ....conftest import (
    MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT,
    MOCK_BASIC_CONFIG_KEYS_COUNT,
)
AGENT_AUTOCOMPLETE_LINE_COUNT = 22
BASIC_CONFIG_AUTOCOMPLETE_AVAILABLE_KEYS_COUNT = 12

KEY_NO_MATCH = 'nomatch'

GROUP_MATCH_TEST = 'demo'
GROUP_NO_GROUP = 'nogroup'
KEY_MATCH_TEST = 'tests/mock/keys/RFC4716/ssh_key_dsa'
KEY_MATCH_MANUAL = 'manual'
KEY_MATCH_MISSING = 'miss*'


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_agent_no_keys(mock_empty_config, mock_agent_no_keys, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list' without any arguments, listing no keys from agent
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err.splitlines() == [NO_KEYS_CONFIGURED]


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_agent_loaded_keys(
        mock_basic_config, mock_agent_key_list, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list' without any arguments, listing no keys from agent
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', '--loaded']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == len(mock_agent_key_list)


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_agent_loaded_autocomplete_keys(
        mock_basic_config, mock_agent_key_list, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list' with arguments to list autocomplete strings for agent keys
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', '--loaded', '--autocomplete']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == AGENT_AUTOCOMPLETE_LINE_COUNT


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_no_keys(mock_empty_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --configured' without any arguments

    This will return with code 1 because there are no keys in mocked empty config
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_configured(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --configured' using mocked basic configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == MOCK_BASIC_CONFIG_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_available(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --available' using mocked basic configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', '--available']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_available_autocomplete(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --available --autocomplete' using mocked basic configuration
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', '--available', '--autocomplete']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == BASIC_CONFIG_AUTOCOMPLETE_AVAILABLE_KEYS_COUNT


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_no_match(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --configured' with key parameters that do not match any keys
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', KEY_NO_MATCH]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=1)

    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_existing(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list with key parameters that match configured keys
    """
    script = SshAssetsScript()
    testargs = ['ssh-assets', 'keys', 'list', KEY_MATCH_TEST, KEY_MATCH_MISSING]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 2


# pylint: disable=unused-argument
def test_ssh_assets_cli_keys_list_match_group(mock_basic_config, monkeypatch, capsys):
    """
    Test running 'ssh-assets keys list --configured' with key parameters that match configured keys both
    by first filtering by group then by key name

    Group matching is done by two group names, one of which is valid
    """
    script = SshAssetsScript()
    group_arg = f'{GROUP_NO_GROUP},{GROUP_MATCH_TEST}'
    testargs = [
        'ssh-assets', 'keys', 'list', '--groups', group_arg, KEY_MATCH_MANUAL, KEY_MATCH_MISSING
    ]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    captured = capsys.readouterr()
    assert captured.err == ''
    # Matches group with 2 keys, but only one matches key names
    assert len(captured.out.splitlines()) == 1
