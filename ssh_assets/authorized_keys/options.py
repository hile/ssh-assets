"""
Parser for OpenSSH authorized keys line command options
"""
import re

from operator import ge, gt, le, lt
from typing import Any, Callable, Tuple, Union

from ..base import RichComparisonObject
from ..exceptions import SSHKeyError
from .constants import AUTHRORIZED_KEYS_OPTION_FLAGS, AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS

RE_OPTION_NAME = r'(?P<option>[a-zAZ0-9-]+)'
RE_OPTION_NO_VALUE = (
    re.compile(f'^{RE_OPTION_NAME},(?P<rest>.*)$'),
    re.compile(f'^{RE_OPTION_NAME}$'),
)
RE_OPTION_WITH_VALUE = (
    re.compile(f'^{RE_OPTION_NAME}="(?P<value>[^"]+)",(?P<rest>.*)$'),
    re.compile(f'^{RE_OPTION_NAME}="(?P<value>[^"]+)"$'),
)


# pylint: disable=too-few-public-methods
class AuthorizedKeyOptionFlag(RichComparisonObject):
    """
    Flag without value in authorized keys options
    """
    option: str

    __compare_attributes__: Tuple[str] = ('option',)

    def __init__(self, option: str) -> None:
        if option not in AUTHRORIZED_KEYS_OPTION_FLAGS:
            raise SSHKeyError(f'Unexpected authorized-keys option flag: {option}')
        self.option = option

    def __repr__(self) -> str:
        return f'{self.option}'


class AuthorizedKeyOptionValue(RichComparisonObject):
    """
    Option with value in authorized keys options
    """
    option: str
    value: str

    __compare_attributes__: Tuple[str] = ('option', 'value')

    def __init__(self, option: str, value: str) -> None:
        if option not in AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS:
            raise SSHKeyError(f'Unexpected authorized-keys option value: {option}={value}')
        self.option = option
        self.value = value

    def __repr__(self) -> str:
        return f'{self.option}="{self.value}"'

    def __compare__(self, operator: Callable, default: bool, other: Any) -> bool:
        """
        Common compare method for sorting
        """
        if isinstance(other, AuthorizedKeyOptionFlag):
            return operator(self.option, other.option)
        return super().__compare__(operator, default, other)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AuthorizedKeyOptionFlag):
            return False
        return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        return self.__compare__(lt, False, other)

    def __gt__(self, other: Any) -> bool:
        return self.__compare__(gt, False, other)

    def __le__(self, other: Any) -> bool:
        return self.__compare__(le, True, other)

    def __ge__(self, other: Any) -> bool:
        return self.__compare__(ge, True, other)


def parse_option_flag(line: str) -> Union[AuthorizedKeyOptionFlag, AuthorizedKeyOptionValue]:
    """
    Match plain authorized key option with no option value in middle of options or end of line'

    This method is called from parser in a loop to digest the options string

    Returns
    ---
    - Option name as AuthorizedKeyOptionFlag or AuthorizedKeyOptionValue object
    - Rest of line without initial , in option string as string or None if end of line is reached
    """
    for pattern in RE_OPTION_NO_VALUE:
        match = pattern.match(line)
        if match:
            data = match.groupdict()
            return AuthorizedKeyOptionFlag(data['option']), data.get('rest', None)

    for pattern in RE_OPTION_WITH_VALUE:
        match = pattern.match(line)
        if match:
            data = match.groupdict()
            return AuthorizedKeyOptionValue(data['option'], data['value']), data.get('rest', None)

    raise SSHKeyError(f'Unexpected data in OpenSSH authorized keys options: {line}')
