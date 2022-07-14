"""
Parser for OpenSSH authorized keys line command options
"""

import re

from operator import ge, gt, le, lt

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


class AuthorizedKeyOptionFlag:
    """
    Flag without value in authorized keys options
    """
    def __init__(self, option):
        if option not in AUTHRORIZED_KEYS_OPTION_FLAGS:
            raise SSHKeyError(f'Unexpected authorized-keys option flag: {option}')
        self.option = option

    def __repr__(self):
        return f'{self.option}'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.option == other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option == getattr(other, 'option', None)

    def __ne__(self, other):
        if isinstance(other, str):
            return self.option != other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option != getattr(other, 'option', None)

    def __lt__(self, other):
        if isinstance(other, str):
            return self.option < other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option < getattr(other, 'option', None)

    def __gt__(self, other):
        if isinstance(other, str):
            return self.option > other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option > getattr(other, 'option', None)

    def __le__(self, other):
        if isinstance(other, str):
            return self.option <= other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option <= getattr(other, 'option', None)

    def __ge__(self, other):
        if isinstance(other, str):
            return self.option >= other
        if not hasattr(other, 'option'):
            raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
        return self.option >= getattr(other, 'option', None)


class AuthorizedKeyOptionValue:
    """
    Option with value in authorized keys options
    """
    __compare_attributes__ = ('option', 'value')

    def __init__(self, option, value):
        if option not in AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS:
            raise SSHKeyError(f'Unexpected authorized-keys option value: {option}={value}')
        self.option = option
        self.value = value

    def __repr__(self):
        return f'{self.option}="{self.value}"'

    def __compare__(self, operator, default, other):
        """
        Common compare method for sorting
        """
        if isinstance(other, AuthorizedKeyOptionFlag):
            return operator(self.option, other.option)
        if isinstance(other, str):
            return operator(str(self), other)
        for attr in self.__compare_attributes__:
            a = getattr(self, attr)
            if not hasattr(other, attr):
                raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
            b = getattr(other, attr)
            if a != b:
                return operator(a, b)
        return default

    def __eq__(self, other):
        if isinstance(other, AuthorizedKeyOptionFlag):
            return False
        if isinstance(other, str):
            return str(self) == other
        for attr in self.__compare_attributes__:
            a = getattr(self, attr)
            if not hasattr(other, attr):
                raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
            b = getattr(other, attr)
            if a != b:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.__compare__(lt, False, other)

    def __gt__(self, other):
        return self.__compare__(gt, False, other)

    def __le__(self, other):
        return self.__compare__(le, True, other)

    def __ge__(self, other):
        return self.__compare__(ge, True, other)


def parse_option_flag(line):
    """
    Match plain authorized key option with no option value in middle of options or end of line'

    This method is called from parser in a loop to digest the options string

    Returns
    ---
    - Option name as string
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
