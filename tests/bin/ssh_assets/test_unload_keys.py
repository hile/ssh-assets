"""
Unit tests for 'ssh-assets load-keys' CLI command
"""

from sys_toolkit.tests.mock import MockCalledMethod

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript

GROUP_MATCH_TEST = 'demo'


# pylint: disable=unused-argument
def test_ssh_assets_unload_keys_invalid_key_name(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets unload-keys' with invalid key name
    """
    mock_method = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.unload_keys_from_agent', mock_method)

    script = SshAssetsScript()
    testargs = ['ssh-assets', 'unload-keys', 'unexpected']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
    assert mock_method.call_count == 1


# pylint: disable=unused-argument
def test_ssh_assets_unload_keys_no_args(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets unload-keys' with no additional arguments

    This command will unload any keys (ssh-add -D) from the agent
    """
    mock_method = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.unload_keys_from_agent', mock_method)

    script = SshAssetsScript()
    testargs = ['ssh-assets', 'unload-keys']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)
    assert mock_method.call_count == 1
    args = mock_method.args[0]
    assert args == ()
    kwargs = mock_method.kwargs[0]
    assert kwargs == {'unload_all_keys': True}


# pylint: disable=unused-argument
def test_ssh_assets_unload_keys_in_group(mock_basic_config, monkeypatch):
    """
    Test running command 'ssh-assets unload-keys' with group name to filter out specific keys
    """
    mock_method = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.keys.agent.SshAgent.unload_keys_from_agent', mock_method)

    script = SshAssetsScript()
    testargs = ['ssh-assets', 'unload-keys', '--groups', GROUP_MATCH_TEST]
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    assert mock_method.call_count == 1
    args = mock_method.args[0]
    assert args == ()
    kwargs = mock_method.kwargs[0]
    assert len(kwargs['keys']) == 2
    assert kwargs['unload_all_keys'] is False
