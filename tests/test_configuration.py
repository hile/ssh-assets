"""
Unit tests for ssh_assets.configuration python module
"""

from ssh_assets.configuration import SshAssetsConfiguration, SshKeyConfiguration
from ssh_assets.keys.file import SSHKeyFile

EXPECTED_KEY_COUNT = 2


def test_load_empty_config(mock_empty_config):
    """
    Test loading empty configuration from mocked empty configuration file
    """
    config = SshAssetsConfiguration()
    assert config.__path__ == mock_empty_config
    assert config.__path__.exists()


def test_load_basic_config(mock_basic_config):
    """
    Test loading basic SSH assets configuration file with basic key details
    """
    config = SshAssetsConfiguration()
    assert config.__path__ == mock_basic_config

    # pylint: disable=no-member
    configured_keys = config.keys
    assert len(configured_keys) == EXPECTED_KEY_COUNT

    for item in configured_keys:
        assert isinstance(item, SshKeyConfiguration)
        assert isinstance(item.__repr__(), str)
        assert isinstance(item.key, SSHKeyFile)
