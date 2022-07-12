"""
Unit tests for ssh_assets.configuration python module
"""

from ssh_assets.session import SshAssetSession
from ssh_assets.configuration import SshAssetsConfiguration, SshKeyConfiguration
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.agent import SshAgentKeys
from ssh_assets.keys.file import SSHKeyFile

EXPECTED_KEY_COUNT = 2
EXPECTED_AVAILABLE_KEY_COUNT = 1


def test_load_empty_config(mock_empty_config):
    """
    Test loading empty configuration from mocked empty configuration file
    """
    session = SshAssetSession()
    assert isinstance(session.configuration, SshAssetsConfiguration)
    assert session.configuration.__path__ == mock_empty_config
    assert session.configuration.__path__.exists()


# pylint: disable=unused-argument
def test_load_basic_config(mock_basic_config, mock_agent_key_list):
    """
    Test loading basic SSH assets configuration file with basic key details
    """
    session = SshAssetSession()
    assert session.configuration.__path__ == mock_basic_config

    # pylint: disable=no-member
    configured_keys = session.configuration.keys
    assert len(configured_keys) == EXPECTED_KEY_COUNT

    for key in configured_keys.available:
        print(key.path)
    assert len(configured_keys.available) == EXPECTED_AVAILABLE_KEY_COUNT

    for item in configured_keys:
        assert isinstance(item, SshKeyConfiguration)
        assert isinstance(item.__repr__(), str)
        assert isinstance(item.key, SSHKeyFile)
        assert isinstance(item.hash_algorithm, KeyHashAlgorithm)
        assert isinstance(item.__agent__, SshAgentKeys)

        if item.available:
            assert isinstance(item.hash, str)
            assert item.loaded is True
        else:
            assert item.hash is None
            assert item.loaded is False
