"""
Module to filter SSH keys loaded in the agent by various methods
"""
from typing import List, Optional, TYPE_CHECKING

from ..configuration.keys import SshKeyConfiguration

if TYPE_CHECKING:
    from ssh_assets.session import SshAssetSession


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
        keys = keys if keys is not None else self.session.user_authorized_keys
