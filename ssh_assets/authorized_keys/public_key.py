"""
SSH keys public key entry in user authorized keys files and exported .pub files
"""
from base64 import b64decode
from typing import List, Tuple, Union

from ..base import RichComparisonObject
from ..exceptions import SSHKeyError

from .constants import SshAuthorizedKeysKeyType
from .options import AuthorizedKeyOptionFlag, AuthorizedKeyOptionValue, parse_option_flag

SSH_KEY_TYPE_STRINGS = [item.value for item in SshAuthorizedKeysKeyType]


# pylint: disable=too-few-public-methods
class PublicKey(RichComparisonObject):
    """
    Entry in OpenSSH authorized keys file
    """
    key_type: str
    base_64: str
    comment: str
    options: List[Union[AuthorizedKeyOptionFlag, AuthorizedKeyOptionValue]]

    __compare_attributes__: Tuple[str] = ('key_type', 'base64',)

    def __init__(self, line: str) -> None:
        self.line = line
        self.key_type, self.base64, self.comment, self.options = self.__parse_line__(line)

    def __repr__(self) -> str:
        return self.line

    def __validate_base64__(self, base64_value: str) -> str:
        """
        Validate the base64 encoded public key value in data is actually valid base64 data
        """
        try:
            b64decode(base64_value)
        except ValueError as error:
            raise SSHKeyError(f'Error parsing {self.line}: invalid base64 encoded public key') from error
        return base64_value

    @staticmethod
    def __parse_options__(option_fields: str) -> List[Union[AuthorizedKeyOptionFlag, AuthorizedKeyOptionValue]]:
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

    def __parse_line__(self, line: str) -> Tuple[
            str, str, str, List[Union[AuthorizedKeyOptionFlag, AuthorizedKeyOptionValue]]]:
        """
        Parse the text entry for authorized keys item
        """
        key_type = None
        base64 = None
        comment = None

        option_fields = []
        fields = line.split(' ')
        for index, field in enumerate(fields):
            if field in SSH_KEY_TYPE_STRINGS:
                try:
                    key_type = SshAuthorizedKeysKeyType(field)
                    base64 = self.__validate_base64__(fields[index + 1])
                    comment = ' '.join(fields[index + 2:])
                    break
                except IndexError as error:
                    raise SSHKeyError(f'Invalid authorized keys line: {line}') from error
            option_fields.append(field)

        options = self.__parse_options__(option_fields)

        return key_type, base64, comment, options
