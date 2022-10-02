"""
Configuration file processing for SSH assets utility
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

import yaml

from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration

from ..exceptions import SSHAssetsError

from .groups import GroupListConfigurationSection
from .keys import SshKeyListConfigurationSection

if TYPE_CHECKING:
    from ..session import SshAssetSession


class SshAssetsConfiguration(YamlConfiguration):
    """
    SSH assets configuration

    User configuration for ssh assets processing python module
    """
    __section_loaders__ = (
        GroupListConfigurationSection,
        SshKeyListConfigurationSection,
    )

    def __init__(self,
                 session: 'SshAssetSession',
                 path: Optional[str] = None,
                 parent: Optional[ConfigurationSection] = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        self.__session__ = session
        super().__init__(path=path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def as_dict(self) -> dict:
        """
        Return configuration as dictionary
        """
        # pylint: disable=no-member
        return {
            'groups': [group.as_dict() for group in self.groups],
            'keys': [key.as_dict() for key in self.keys],
        }

    def as_yaml(self) -> str:
        """
        Return configuration as YAML stream
        """
        return yaml.dump(self.as_dict(), Dumper=SSHAssetsConfigurationDumper)

    def save(self, path: Optional[str] = None) -> None:
        """
        Save configuration to specified file. If not path is specified original path is used.
        """
        path = Path(path).expanduser().resolve() if path is not None else self.__path__
        data = self.as_yaml()
        try:
            path.write_text(data, encoding='utf-8')
        except OSError as error:
            raise SSHAssetsError(f'Error writing file {path}: {error}') from error


class SSHAssetsConfigurationDumper(yaml.Dumper):
    """
    YAML dumper for SSH assets configuration file saving that indents lists with 2 spaces
    """
    # pylint: disable=unused-argument
    def increase_indent(self, *args, flow=False, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)
