"""
Class to load OpenSSH authorized keys files
"""

from base64 import b64decode
from pathlib import Path

from sys_toolkit.collection import CachedMutableSequence

from ..exceptions import SSHKeyError

from .constants import KEY_TYPES
from .options import parse_option_flag


# pylint: disable=too-few-public-methods
class AuthorizedKeyEntry:
    """
    Entry in OpenSSH authorized keys file
    """
    def __init__(self, line):
        self.line = line
        self.key_type, self.base64, self.options, self.comment = self.__parse_line__(line)

    def __repr__(self) -> str:
        return self.line

    def __validate_base64__(self, base64_value):
        """
        Validate the base64 encoded public key value in data is actually valid base64 data
        """
        try:
            b64decode(base64_value)
        except ValueError as error:
            raise SSHKeyError(f'Error parsing {self.line}: invalid base64 encoded public key') from error
        return base64_value

    @staticmethod
    def __parse_options__(option_fields):
        """
        Parse options from specified option string
        """
        options = []
        line = ' '.join(option_fields)
        if line != '':
            while line is not None:
                option, rest = parse_option_flag(line)
                options.append(option)
                line = rest
        return options

    def __parse_line__(self, line):
        """
        Parse the text entry for authorized keys item
        """
        key_type = None
        base64 = None
        comment = None

        option_fields = []
        fields = line.split(' ')
        for index, field in enumerate(fields):
            if field in KEY_TYPES:
                try:
                    key_type = field
                    base64 = self.__validate_base64__(fields[index + 1])
                    comment = ' '.join(fields[index + 2:])
                    break
                except IndexError as error:
                    raise SSHKeyError(f'Invalid authorized keys line: {line}') from error
            option_fields.append(field)

        options = self.__parse_options__(option_fields)

        return key_type, base64, options, comment


class AuthorizedKeys(CachedMutableSequence):
    """
    List of OpenSSH authorized keys items
    """
    def __init__(self, path):
        super().__init__()
        self.path = Path(path).expanduser().resolve()

    def update(self):
        """
        Update items in authorized keys file data by reading the file
        """
        self.__start_update__()
        self.__items__ = []

        if not self.path.is_file():
            raise SSHKeyError(f'Error loading SSH authorized keys list: No such file: {self.path}')

        try:
            data = self.path.read_text(encoding='utf-8')
            for line in data.splitlines():
                if line.strip() == '' or line.startswith('#'):
                    continue
                self.__items__.append(AuthorizedKeyEntry(line))
        except OSError as error:
            raise SSHKeyError(f'Error loading SSH authorized keys list from {self.path}: {error}') from error

        self.__finish_update__()
