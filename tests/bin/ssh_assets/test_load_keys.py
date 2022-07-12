"""
Unit tests for ssh-assets main CLI class
"""

from sys_toolkit.tests.mock import MockCalledMethod

from cli_toolkit.tests.script import validate_script_run_exception_with_args

from ssh_assets.bin.ssh_assets.main import SshAssetsScript


def test_ssh_assets_load_keys_no_args(monkeypatch):
    """
    Test running command 'ssh-assets load-keys' with no additional arguments
    """
    mock_method = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.session.SshAssetSession.load_available_keys', mock_method)

    script = SshAssetsScript()
    testargs = ['ssh-assets', 'load-keys']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    assert mock_method.call_count == 1
    args = mock_method.args[0]
    assert args == ()
    kwargs = mock_method.kwargs[0]
    assert kwargs == {'load_all_keys': False}


def test_ssh_assets_load_keys_all_keys(monkeypatch):
    """
    Test running command 'ssh-assets load-keys' with all keys to load specified explicitly
    """
    mock_method = MockCalledMethod()
    monkeypatch.setattr('ssh_assets.session.SshAssetSession.load_available_keys', mock_method)

    script = SshAssetsScript()
    testargs = ['ssh-assets', 'load-keys', '--all']
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(script, context, testargs, exit_code=0)

    assert mock_method.call_count == 1
    args = mock_method.args[0]
    assert args == ()
    kwargs = mock_method.kwargs[0]
    assert kwargs == {'load_all_keys': True}
