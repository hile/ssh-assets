"""
Configuration parser for 'groups' configuration section in SSH assets configuration
"""
from typing import List, Optional, TYPE_CHECKING

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection

from ..duration import Duration

if TYPE_CHECKING:
    from .keys import SshKeyConfiguration, SshKeyListConfigurationSection


class GroupConfiguration(ConfigurationSection):
    """
    Configuration section for a single group in 'groups' configuration section
    """
    __name__ = 'group'
    name: Optional[str] = None
    expire: Optional[bool] = None
    keys: Optional['SshKeyConfiguration'] = None
    __default_settings__ = {
        'expire': None,
        'keys': [],
    }
    __required_settings__ = (
        'name',
    )

    def __init__(self,
                 data: dict = dict,
                 parent: ConfigurationSection = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        super().__init__(data, parent, debug_enabled, silent)
        self.expire = Duration(self.expire) if self.expire is not None else None

    def __repr__(self) -> str:
        return self.name if self.name else ''

    @property
    def __key_configuration__(self) -> 'SshKeyListConfigurationSection':
        """
        Return reference to the key configuration section
        """
        return self.__parent__.__parent__.keys  # pylint: disable=no-member

    @property
    def private_keys(self) -> List['SshKeyConfiguration']:
        """
        Return private key configuration items matching this group
        """
        return [key for key in self.__key_configuration__ if key.name in self.keys]

    def as_dict(self) -> dict:
        """
        Return key configuration section as dictionary
        """
        data = {
            'name': self.name,
        }
        if self.keys:
            data['keys'] = [str(key) for key in self.keys]
        if self.expire:
            data['expire'] = str(self.expire)
        return data

    def update(self, **kwargs) -> bool:
        """
        Update group attributes from kwargs

        Kwargs can contain valid updated values for path, expire and autoload fields

        Returns
        -------
        True if any of the fields were changed
        """
        modified = False
        if 'keys' in kwargs:
            keys = kwargs['keys']
            if not isinstance(keys, list):
                raise ValueError('Keys must be list of key names')
            if sorted(keys) != sorted(self.keys):
                for name in keys:
                    if not self.__key_configuration__.get_key_by_name(name):
                        raise ValueError(f'Invalid key name: {name}')
                self.keys = keys
                modified = True
        if 'expire' in kwargs:
            expire = kwargs['expire']
            if expire is not None:
                expire = Duration(expire)
            if self.expire != expire:
                self.expire = expire
                modified = True
        return modified


class GroupListConfigurationSection(ConfigurationList):
    """
    Configuration section for gropus list
    """
    __dict_loader_class__ = GroupConfiguration
    __name__ = 'groups'

    def get_group_by_name(self, name: str) -> GroupConfiguration:
        """
        Return configured group by name

        Returns
        -------
        GroupConfiguration object or None if named group does not exist
        """
        for group in self:
            if group.name == name:
                return group
        return None

    def configure_group(self, name: str, **kwargs) -> None:
        """
        Configure named group to the SSH assets configuration and save configuration file
        """
        group = self.get_group_by_name(name)
        if group is None:
            kwargs['name'] = name
            group = GroupConfiguration(parent=self, data=kwargs)
            self.append(group)
            modified = True
        else:
            modified = group.update(**kwargs)
        if modified:
            self.__parent__.save()
