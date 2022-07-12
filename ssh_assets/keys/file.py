"""
Classes to load SSH keys from text files
"""

from pathlib import Path

from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run_command_lineoutput

from ..exceptions import SSHKeyError
from .base import SSHKeyLoader
from .constants import DEFAULT_KEY_HASH_ALGORITHM


class SSHKeyFile(SSHKeyLoader):
    """SSH key file base class

    Base class for SSH private and public keys based on text files
    """
    def __init__(self, path, hash_algorithm=DEFAULT_KEY_HASH_ALGORITHM):
        super().__init__(hash_algorithm)
        self.path = Path(path).expanduser().resolve()

    def __repr__(self):
        return str(self.path)

    def __load_key_attributes__(self):
        """
        Load key attributes with ssh-keygen -l command
        """
        if not self.path.is_file():
            raise SSHKeyError(f'Error loading SSH key attributes: no such file: {self.path}')

        try:
            stdout, _stderr = run_command_lineoutput(
                'ssh-keygen', '-E', self.hash_algorithm.value, '-l', '-f', str(self.path)
            )
        except CommandError as error:
            raise SSHKeyError(f'Error loading SSH key attributes: {error}') from error

        if not stdout:
            raise SSHKeyError('Error loading SSH key attributes: command output is empty')

        return self.__parse_key_info_line__(stdout[0])
