"""
Module to filter SSH keys loaded in the agent by various methods
"""
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from ..configuration.groups import GroupConfiguration
from ..configuration.keys import SshKeyConfiguration

if TYPE_CHECKING:
    from ssh_assets.session import SshAssetSession


def filter_key_groups(session: 'SshAssetSession',
                      keys: List[SshKeyConfiguration],
                      groups: List[Union[str, GroupConfiguration]]) -> List[SshKeyConfiguration]:
    """
    Filter list of keys by key group name
    """
    def match_groups(groups: List[str], key) -> bool:
        """
        Match key groups to list of groups
        """
        for group in groups:
            if key.name in group.keys:
                return True
        return False

    if not groups:
        return list(keys)

    group_matches = []
    for item in groups:
        group = session.configuration.groups.get_group_by_name(item)
        if group:
            group_matches.append(group)

    matches = []
    for key in keys:
        if match_groups(group_matches, key):
            matches.append(key)
    return matches


def filter_key_names(keys: List[SshKeyConfiguration], names: List[str]) -> List[SshKeyConfiguration]:
    """
    Filter list of keys by key name
    """
    def match_keys(patterns: List[str], name: str):
        """
        Match specified key name to list of strings
        """
        for pattern in patterns:
            if fnmatch(name, pattern):
                return True
        return False

    if not names:
        return list(keys)

    paths = [Path(arg).expanduser().resolve() for arg in names]

    matches = []
    for key in keys:
        full_path = key.path.expanduser().resolve()
        if match_keys(names, key.name) or full_path in paths:
            matches.append(key)
    return matches


def filter_key_available(keys: List[SshKeyConfiguration], available: bool = True) -> List[SshKeyConfiguration]:
    """
    Filter list of keys by key available flag status
    """
    return [key for key in keys if key.available == available]


def filter_key_loaded(keys: List[SshKeyConfiguration], loaded: bool = True) -> List[SshKeyConfiguration]:
    """
    Filter list of keys by key loaded flag status
    """
    return [key for key in keys if key.loaded == loaded]


# pylint: disable=too-few-public-methods
class SshKeyFilterSet:
    """
    SSH key filter set
    """
    session: 'SshAssetSession'
    keys: List[SshKeyConfiguration]

    def __init__(self,
                 session: 'SshAssetSession',
                 keys: Optional[List[SshKeyConfiguration]] = None) -> None:
        self.session = session
        self.keys = keys if keys is not None else list(self.session.configuration.keys)

    def filter_available(self, available: bool = True) -> 'SshKeyFilterSet':
        """
        Filter keys by 'available' flag value
        """
        return SshKeyFilterSet(self.session, filter_key_available(self.keys, available))

    def filter_groups(self, groups: List[Union[str, GroupConfiguration]]) -> 'SshKeyFilterSet':
        """
        Filter keys by groups or group names
        """
        return SshKeyFilterSet(self.session, filter_key_groups(self.session, self.keys, groups))

    def filter_loaded(self, loaded: bool = True) -> 'SshKeyFilterSet':
        """
        Filter keys by 'loaded' flag value
        """
        return SshKeyFilterSet(self.session, filter_key_loaded(self.keys, loaded))

    def filter_names(self, names: List[str]) -> 'SshKeyFilterSet':
        """
        Filter keys by names
        """
        return SshKeyFilterSet(self.session, filter_key_names(self.keys, names))
