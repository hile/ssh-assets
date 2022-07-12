"""
SSH assets manager session
"""

from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run_command

from .constants import USER_CONFIGURATION_FILE
from .configuration import SshAssetsConfiguration
from .exceptions import SSHKeyError
from .keys.agent import SshAgentKeys


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
        return SshAgentKeys(self)

    def unload_keys(self):
        """
        Unload all keys from SSH agent
        """
        if not self.agent.is_available:
            raise SSHKeyError('SSH agent is not configured')

        try:
            run_command('ssh-add', '-D')
        except CommandError as error:
            raise SSHKeyError(f'Error unloading SSH keys from agent: {error}') from error

    def load_pending_keys(self):
        """
        Load any available configured keys not yet loaded to the agent
        """
        # pylint: disable=no-member
        for configured_key in self.configuration.keys.pending:
            configured_key.load_to_agent()
