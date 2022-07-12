"""
Configuration file processing for SSH assets utility
"""

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration

from .keys.file import SSHKeyFile


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

    @property
    def __agent__(self):
        """
        Return handle to the ssh_assets.keys.agent.SshAgentKeys object via session
        """
        return self.__parent__.__parent__.__session__.agent

    @property
    def hash_algorithm(self):
        """
        Return hash for key from file details if key is available
        """
        return self.key.hash_algorithm

    @property
    def hash(self):
        """
        Return hash for key from file details if key is available
        """
        if not self.path.is_file():
            return None
        return self.key.hash

    @property
    def available(self):
        """
        Check if this key file is available for loading to SSH agent
        """
        return self.path.is_file()

    @property
    def loaded(self):
        """
        Check if this key is loaded to the SSH agent

        May fail if key file is not available
        """
        if not self.path.is_file():
            return False
        return self.key.hash in self.__agent__

    def load_to_agent(self):
        """
        Load configured key to SSH agent
        """
        self.key.load_to_agent()


class SSHKeyListConfigurationSection(ConfigurationList):
    """
    Configuration section for SSH key usage
    """
    __dict_loader_class__ = SshKeyConfiguration
    __name__ = 'keys'

    @property
    def available(self):
        """
        Return avaiable configured SSH keys
        """
        return [key for key in self if key.available]

    @property
    def pending(self):
        """
        Return available and autoloaded configured SSH keys not yet loaded to agent
        """
        return [key for key in self if key.available and key.autoload and not key.loaded]


class SshAssetsConfiguration(YamlConfiguration):
    """
    SSH assets configuration

    User configuration for ssh assets processing python module
    """
    __section_loaders__ = (
        SSHKeyListConfigurationSection,
    )

    def __init__(self, session, path=None, parent=None, debug_enabled=False, silent=False):
        self.__session__ = session
        super().__init__(path=path, parent=parent, debug_enabled=debug_enabled, silent=silent)
