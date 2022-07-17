"""
Configuration file processing for SSH assets utility
"""

import yaml

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

    def as_dict(self):
        """
        Return configuration as dictionary
        """
        # pylint: disable=no-member
        return {
            'groups': [group.as_dict() for group in self.groups],
            'keys': [key.as_dict() for key in self.keys],
        }

    def as_yaml(self):
        """
        Return configuration as YAML stream
        """
        return yaml.dump(self.as_dict(), Dumper=SSHAssetsConfigurationDumper)


class SSHAssetsConfigurationDumper(yaml.Dumper):
    """
    YAML dumper for SSH assets configuration file saving that indents lists with 2 spaces
    """
    # pylint: disable=unused-argument
    def increase_indent(self, *args, flow=False, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)
