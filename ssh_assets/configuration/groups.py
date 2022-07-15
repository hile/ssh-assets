"""
Configuration parser for 'groups' configuration section in SSH assets configuration
"""

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection


class GroupConfiguration(ConfigurationSection):
    """
    Configuration section for a single group in 'groups' configuration section
    """
    __name__ = 'group'
    name = None
    expire = None
    keys: None
    __default_settings__ = {
        'expire': None,
        'keys': [],
    }
    __required_settings__ = (
        'name',
    )

    def __repr__(self):
        return self.name if self.name else ''

    @property
    def __key_configuration__(self):
        """
        Return reference to the key configuration section
        """
        return self.__parent__.__parent__.keys  # pylint: disable=no-member

    @property
    def private_keys(self):
        """
        Return private key configuration items matching this group
        """
        return [key for key in self.__key_configuration__ if key.name in self.keys]


class GroupListConfigurationSection(ConfigurationList):
    """
    Configuration section for gropus list
    """
    __dict_loader_class__ = GroupConfiguration
    __name__ = 'groups'
