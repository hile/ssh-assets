"""
Configuration parser for 'keys' configuration section in SSH assets configuration
"""

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection
from ..keys.file import SSHKeyFile


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
        self.private_key = SSHKeyFile(self.path)

    def __repr__(self):
        return str(self.name) if self.name else ''

    @property
    def __agent__(self):
        """
        Return handle to the ssh_assets.keys.agent.SshAgentKeys object via session
        """
        return self.__parent__.__parent__.__session__.agent

    @property
    def __group_configuration__(self):
        """
        Return reference to the groups configuration section
        """
        return self.__parent__.__parent__.groups  # pylint: disable=no-member

    @property
    def hash_algorithm(self):
        """
        Return hash for key from file details if key is available
        """
        return self.private_key.hash_algorithm

    @property
    def hash(self):
        """
        Return hash for key from file details if key is available
        """
        if not self.path.is_file():
            return None
        return self.private_key.hash

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
        return self.private_key.hash in self.__agent__

    @property
    def groups(self):
        """
        Return groups where this key is referenced
        """
        return [group for group in self.__group_configuration__ if self.name in group.keys]

    def load_to_agent(self):
        """
        Load configured key to SSH agent
        """
        self.private_key.load_to_agent()


class SshKeyListConfigurationSection(ConfigurationList):
    """
    Configuration section for SSH keys list
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
