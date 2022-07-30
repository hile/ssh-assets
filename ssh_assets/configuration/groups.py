"""
Configuration parser for 'groups' configuration section in SSH assets configuration
"""

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection

from ..duration import Duration


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

    def __init__(self, data=dict, parent=None, debug_enabled=False, silent=False):
        super().__init__(data, parent, debug_enabled, silent)
        self.expire = Duration(self.expire) if self.expire is not None else None

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

    def as_dict(self):
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

    def update(self, **kwargs):
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
                raise ValueError(f'Keys must be list of key names')
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

    def get_group_by_name(self, name):
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

    def configure_group(self, name, **kwargs):
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
