"""
Classes to load SSH keys from text files
"""

from pathlib import Path

from sys_toolkit.exceptions import CommandError
from sys_toolkit.subprocess import run_command, run_command_lineoutput

from ..authorized_keys.public_key import PublicKey
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

    @property
    def public_key_file_path(self):
        """
        Return pathlib.Path of self.path with .pub extension added
        """
        return Path(f'{self.path}.pub') if self.path.suffix != '.pub' else None

    @property
    def has_public_key_file(self):
        """
        Return boolen to indicate if public key file for this SSH key exists
        """
        return self.public_key_file_path.is_file() if self.public_key_file_path is not None else False

    @property
    def public_key(self):
        """
        Return public key object from previously generated public key file
        """
        if not self.has_public_key_file:
            raise SSHKeyError(f'Key has no .pub public key file: {self.public_key_file_path}')
        try:
            return PublicKey(self.public_key_file_path.read_text(encoding='utf-8').strip())
        except OSError as error:
            raise SSHKeyError(f'Error reading public key file {self.public_key_file_path}: {error}') from error

    def unload_from_agent(self):
        """
        Unlad SSH key from agent
        """
        try:
            run_command('ssh-add', '-d', str(self.path))
        except CommandError as error:
            raise SSHKeyError(f'Error unloading key from SSH agent: {error}') from error

    def load_to_agent(self, expire=None):
        """
        Load SSH key to agent
        """
        if expire:
            command = ('ssh-add', '-t', str(expire), str(self.path))
        else:
            command = ('ssh-add', str(self.path))
        try:
            run_command(*command)
        except CommandError as error:
            raise SSHKeyError(f'Error loading key to SSH agent: {error}') from error

    def generate_public_key_file(self, filename=None, force=False):
        """
        Get matching .pub public key file for this key

        Note: this command will ask SSH key passphrase interactively if the .pub file does not
        exist and private key requires passphrase

        Arguments
        ---------
        filename:   Filename for the generated file. By default .pub extension is added to self.path
        force:      Overwrite existing output file if force=True

        Returns
        -------
        Filename of public key as pathlib.Path
        """
        if not self.path.is_file():
            raise SSHKeyError(f'Error exporting public key file from {self.path}: no such file')

        filename = Path(filename).expanduser() if filename is not None else self.public_key_file_path
        if force or not filename.exists():
            try:
                stdout, _stderr = run_command_lineoutput('ssh-keygen', '-y', '-f', str(self.path))
            except CommandError as error:
                raise SSHKeyError(f'Error exporting public key file from {self.path}: {error}') from error
            try:
                with filename.open('w', encoding='utf-8') as handle:
                    data = '\n'.join(stdout)
                    handle.write(f'{data}\n')
            except OSError as error:
                raise SSHKeyError(f'Error exporting public key file to {filename}: {error}') from error
        return filename
