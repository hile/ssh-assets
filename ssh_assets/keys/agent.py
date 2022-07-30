"""
SSH agent client

Allows listing, loading and flushing SSH keys loaded to SSH agent
"""

import os
from pathlib import Path

from sys_toolkit.collection import CachedMutableSequence
from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run_command_lineoutput, run_command

from ..exceptions import SSHKeyError

from .base import SSHKeyLoader
from .constants import (
    DEFAULT_KEY_HASH_ALGORITHM,
    SSH_AUTH_SOCK_ENV_VAR,
    SSH_AGENT_NO_KEYS_MESSAGE,
)


class AgentKey(SSHKeyLoader):
    """
    SSH key details from SSH agent key listing
    """
    def __init__(self, line, hash_algorithm):
        super().__init__(hash_algorithm)
        self.line = line
        self.__parse_key_info_line__(line)

    def __repr__(self):
        return self.line

    def __load_key_attributes__(self):
        """
        This method is not required for agent keys, because the key data is provided
        when object is initialized by 'line' parameter
        """
        return


class SshAgent(CachedMutableSequence):
    """
    Class to list, load and flush keys from ssh agent
    """
    def __init__(self, session, hash_algorithm=DEFAULT_KEY_HASH_ALGORITHM):
        self.session = session
        self.hash_algorithm = hash_algorithm

    @property
    def configured_keys(self):
        """
        Return SSH keys configured in the SSH assets configuration file
        """
        # pylint: disable=no-member
        return self.session.configuration.keys

    @property
    def agent_socket_path(self):
        """
        Return SSH agent socket path from environment variable
        """
        return os.environ.get(SSH_AUTH_SOCK_ENV_VAR, None)

    @property
    def is_available(self):
        """
        Check if SSH agent is configured

        - checks if SSH_AUTH_SOCK environment variable is defined
        - if the variable points to existing socket file
        - if the socket is readable and writable by current user
        """
        path = self.agent_socket_path
        if not path:
            return False
        if not Path(path).is_socket():
            return False
        return os.access(path, os.R_OK | os.W_OK)

    def update(self):
        """
        Update list of keys loaded to the ssh agent
        """
        self.__start_update__()
        self.__items__ = []
        try:
            stdout, _stderr = run_command_lineoutput(
                'ssh-add', '-E', self.hash_algorithm.value, '-l',
                expected_return_codes=(0, 1)
            )
        except CommandError as error:
            self.__reset__()
            raise SSHKeyError(f'Error listing SSH keys loaded to ssh-agent: {error}') from error

        if len(stdout) == 1 and stdout[0] == SSH_AGENT_NO_KEYS_MESSAGE:
            stdout = []

        for line in stdout:
            self.append(AgentKey(line, self.hash_algorithm))

        self.__finish_update__()

    @staticmethod
    def unload_keys_from_agent(keys=None, unload_all_keys=False):
        """
        Unload any named or configured keys from SSH agent

        If unload_all_keys is True, all keys are removed from the agent
        """
        if unload_all_keys:
            try:
                run_command('ssh-add', '-D')
            except CommandError as error:
                raise SSHKeyError(f'Error unloading SSH keys from agent: {error}') from error

        if not keys:
            return

        for key in keys:
            if key.loaded:
                key.unload_from_agent()

    def load_keys_to_agent(self, keys=None, load_all_keys=False):
        """
        Load any available configured keys

        If load_all_keys is False, only keys mared as autoload are loaded
        """
        if not keys:
            keys = self.configured_keys
        for key in keys:
            if not load_all_keys and not key.autoload:
                continue
            if not key.loaded and key.available:
                key.load_to_agent()
                if key.minimum_expire:
                    self.session.configuration.message(f'key {key} loaded with expiration value {key.minimum_expire}')
