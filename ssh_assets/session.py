"""
SSH assets manager session
"""

from .authorized_keys import AuthorizedKeys
from .constants import USER_CONFIGURATION_FILE
from .configuration import SshAssetsConfiguration
from .keys.agent import SshAgent


# pylint: disable=too-few-public-methods
class SshAssetSession:
    """
    SSH asset manager session

    This class binds asset manager configuration, SSH agent client and other resources
    together
    """
    def __init__(self, configuration_file=None):
        configuration_file = configuration_file if configuration_file is not None else USER_CONFIGURATION_FILE
        self.configuration = SshAssetsConfiguration(self, configuration_file)

    @property
    def agent(self):
        """
        Return SSH agent object

        This is initialized separately on each call intentionally to trigger lookup for loaded keys
        """
        return SshAgent(self)

    @property
    def user_authorized_keys(self):
        """
        Return SSH authorized keys parser object for user default authorized keys file

        This is initialized separately on each call intentionally to trigger lookup for loaded keys
        """
        return AuthorizedKeys()
