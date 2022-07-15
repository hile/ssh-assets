"""
Configuration file processing for SSH assets utility
"""

from sys_toolkit.configuration.yaml import YamlConfiguration

from .groups import GroupListConfigurationSection
from .keys import SshKeyListConfigurationSection


class SshAssetsConfiguration(YamlConfiguration):
    """
    SSH assets configuration

    User configuration for ssh assets processing python module
    """
    __section_loaders__ = (
        GroupListConfigurationSection,
        SshKeyListConfigurationSection,
    )

    def __init__(self, session, path=None, parent=None, debug_enabled=False, silent=False):
        self.__session__ = session
        super().__init__(path=path, parent=parent, debug_enabled=debug_enabled, silent=silent)
