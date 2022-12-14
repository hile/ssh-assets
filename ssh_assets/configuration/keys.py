"""
Configuration parser for 'keys' configuration section in SSH assets configuration
"""
from operator import eq, ne, ge, gt, le, lt
from pathlib import Path
from typing import List, Optional

from sys_toolkit.configuration.base import ConfigurationList, ConfigurationSection

from .groups import GroupConfiguration, GroupListConfigurationSection
from ..duration import Duration
from ..keys.agent import SshAgent
from ..keys.file import SSHKeyFile


class SshKeyConfiguration(ConfigurationSection):
    """
    Configuration section for a single SSH key
    """
    name: str = None
    path: Path = None
    autoload: bool = False
    expire: Optional[Duration] = None
    __literal_path__: Optional[Path] = None

    __required_settings__ = (
        'name',
        'path',
    )

    def __init__(self,
                 data: dict = dict,
                 parent: ConfigurationSection = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        super().__init__(data, parent, debug_enabled, silent)
        self.expire = Duration(self.expire) if self.expire is not None else None
        self.private_key = SSHKeyFile(self.path)

    def __compare_method__(self, other, method, default: bool) -> int:
        """
        Deep compare for keys
        """
        if isinstance(other, str):
            return method(self.name, other)
        for attr in ('name', 'path'):
            a = getattr(self, attr)
            b = getattr(other, attr)
            if a != b:
                return method(a, b)
        return default

    def __eq__(self, other):
        return self.__compare_method__(other, eq, True)

    def __ne__(self, other):
        return self.__compare_method__(other, ne, False)

    def __ge__(self, other):
        return self.__compare_method__(other, ge, True)

    def __gt__(self, other):
        return self.__compare_method__(other, gt, False)

    def __le__(self, other):
        return self.__compare_method__(other, le, True)

    def __lt__(self, other):
        return self.__compare_method__(other, lt, True)

    def __repr__(self) -> str:
        return str(self.name) if self.name else ''

    def __setattr__(self, attr, value):
        """
        Override __setattr__ to store original value of path to __literal_path__
        """
        if attr == 'path':
            self.__literal_path__ = value
            if value is not None:
                value = Path(value).expanduser().resolve()
        super().__setattr__(attr, value)

    @property
    def __agent__(self) -> SshAgent:
        """
        Return handle to the ssh_assets.keys.agent.SshAgent object via session
        """
        return self.__parent__.__parent__.__session__.agent

    @property
    def __group_configuration__(self) -> GroupListConfigurationSection:
        """
        Return reference to the groups configuration section
        """
        return self.__parent__.__parent__.groups  # pylint: disable=no-member

    @property
    def hash_algorithm(self) -> str:
        """
        Return hash for key from file details if key is available
        """
        return self.private_key.hash_algorithm

    @property
    def hash(self) -> str:
        """
        Return hash for key from file details if key is available
        """
        if not self.path.is_file():
            return None
        return self.private_key.hash

    @property
    def available(self) -> bool:
        """
        Check if this key file is available for loading to SSH agent
        """
        return self.path.is_file()

    @property
    def loaded(self) -> bool:
        """
        Check if this key is loaded to the SSH agent

        May fail if key file is not available
        """
        if not self.path.is_file():
            return False
        return self.private_key.hash in self.__agent__

    @property
    def minimum_expire(self) -> Optional[Duration]:
        """
        Return shortest configured expiration value from key and it's groups
        """
        values = [self.expire] if self.expire else []
        for group in self.groups:
            if group.expire:
                values.append(group.expire)
        if values:
            return sorted(values)[-1]
        return None

    @property
    def groups(self) -> List[GroupConfiguration]:
        """
        Return groups where this key is referenced
        """
        return [group for group in self.__group_configuration__ if self.name in group.keys]

    def unload_from_agent(self) -> None:
        """
        Unload configured key from SSH agent
        """
        self.private_key.unload_from_agent()

    def load_to_agent(self) -> None:
        """
        Load configured key to SSH agent
        """
        self.private_key.load_to_agent(expire=self.minimum_expire)

    def as_dict(self) -> dict:
        """
        Return key configuration section as dictionary
        """
        data = {
            'name': self.name,
            'path': str(self.__literal_path__),
        }
        if self.expire is not None:
            data['expire'] = str(self.expire)
        if self.autoload:
            data['autoload'] = True
        return data

    def update(self, **kwargs) -> bool:
        """
        Update key attributes from kwargs

        Kwargs can contain valid updated values for path, expire and autoload fields

        Returns
        -------
        True if any of the fields were changed
        """
        modified = False
        path = kwargs.get('path', None)
        if path and self.__literal_path__ != path:
            self.path = path
            modified = True
        if 'autoload' in kwargs and kwargs['autoload'] in (True, False, None):
            if self.autoload != kwargs['autoload']:
                self.autoload = kwargs['autoload']
                modified = True
        if 'expire' in kwargs:
            expire = kwargs['expire']
            if expire is not None:
                expire = Duration(expire)
            if self.expire != expire:
                self.expire = expire
                modified = True
        return modified


class SshKeyListConfigurationSection(ConfigurationList):
    """
    Configuration section for SSH keys list
    """
    __dict_loader_class__ = SshKeyConfiguration
    __name__ = 'keys'

    def __init__(self,
                 setting: Optional[str] = None,
                 data: Optional[dict] = None,
                 parent: ConfigurationSection = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        super().__init__(setting, data, parent)
        self.__key_name_lookup__ = {}

    def __delitem__(self, key: SshKeyConfiguration) -> None:
        """
        Delete specified key from configuration
        """
        for index, item in enumerate(self.__values__):
            if item == key:
                del self.__values__[index]
                del self.__key_name_lookup__[item.name]
                break

    @property
    def available(self) -> List[SshKeyConfiguration]:
        """
        Return avaiable configured SSH keys
        """
        return [key for key in self if key.available]

    @property
    def pending(self) -> List[SshKeyConfiguration]:
        """
        Return available and autoloaded configured SSH keys not yet loaded to agent
        """
        return [key for key in self if key.available and key.autoload and not key.loaded]

    def append(self, value: SshKeyConfiguration) -> None:
        """
        Append an item to the key configuration
        """
        self.__key_name_lookup__[value.name] = value
        super().append(value)

    def get_key_by_name(self, name: str) -> SshKeyConfiguration:
        """
        Get key by name
        """
        try:
            return self.__key_name_lookup__[name]
        except KeyError:
            return None

    def delete_key(self, name: str) -> None:
        """
        Delete named eky from configuration
        """
        modified = False
        key = self.get_key_by_name(name)
        if key:
            del self[key.name]
            modified = True
        if modified:
            self.__parent__.save()

    def configure_key(self, name: str, **kwargs) -> None:
        """
        Configure named key to the SSH assets configuration and save configuration file
        """
        key = self.get_key_by_name(name)
        if key is None:
            kwargs['name'] = name
            key = SshKeyConfiguration(parent=self, data=kwargs)
            self.append(key)
            modified = True
        else:
            modified = key.update(**kwargs)
        if modified:
            self.__parent__.save()
