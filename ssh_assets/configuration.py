"""
Configuration file processing for SSH assets utility
"""

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration

from .keys.file import SSHKeyFile
from .constants import USER_CONFIGURATION_FILE


class SshKeyConfiguration(ConfigurationSection):
    """
    Configuration section for a single SSH key
    """
    name = None
    path = None
    expire = None
    autoload = False

    __required_settings__ = (
        'name',
        'path',
    )
    __path_settings__ = (
        'path',
    )

    def __init__(self, data=dict, parent=None, debug_enabled=False, silent=False):
        super().__init__(data, parent, debug_enabled, silent)
        self.key = SSHKeyFile(self.path)

    def __repr__(self):
        return str(self.name) if self.name else ''


class SSHKeyListConfigurationSection(ConfigurationList):
    """
    Configuration section for SSH key usage
    """
    __dict_loader_class__ = SshKeyConfiguration
    __name__ = 'keys'


class SshAssetsConfiguration(YamlConfiguration):
    """
    SSH assets configuration

    User configuration for ssh assets processing python module
    """
    __section_loaders__ = (
        SSHKeyListConfigurationSection,
    )

    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False):
        path = path if path is not None else USER_CONFIGURATION_FILE
        super().__init__(path=path, parent=parent, debug_enabled=debug_enabled, silent=silent)
