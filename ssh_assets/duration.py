"""
Utility functions for ssh_assets module
"""

import re

from datetime import timedelta
from typing import Any, Tuple

RE_TIME_VALUE = re.compile(r'^(?P<value>\d+)(?P<qualifier>[smhdw])(?P<rest>.*)$')

SECONDS_MULTIPLIERS = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
    'w': 604800,
}


class Duration:
    """
    Time duration string as defined in 'TIME FORMATS' section of sshd manual page
    """
    def __init__(self, value: str) -> None:
        self.__fields__ = {
            's': None,
            'm': None,
            'h': None,
            'd': None,
            'w': None,
        }
        self.__parse_value__(value)

    def __repr__(self) -> str:
        """
        Return duration as string, with fields ordered correctly
        """
        return ''.join(
            f'{value}{key}'
            for key, value in self.__fields__.items() if value is not None
        )

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: Any) -> bool:
        return str(self) != str(other)

    def __lt__(self, other: Any) -> bool:
        return str(self) < str(other)

    def __gt__(self, other: Any) -> bool:
        return str(self) > str(other)

    def __le__(self, other: Any) -> bool:
        return str(self) <= str(other)

    def __ge__(self, other: Any) -> bool:
        return str(self) >= str(other)

    @staticmethod
    def __parse_duration_field__(value: str) -> Tuple[str, int, str]:
        """
        Get a single time value from specified string

        Returns
        -------
        qualifier, value, rest tuple
        qualifier is valid key in self.__fields__
        value is a valid
        """
        match = RE_TIME_VALUE.match(value)
        if match:
            qualifier = match['qualifier']
            value = int(match['value'])
            rest = match['rest']
        else:
            qualifier = 's'
            value = int(value)
            rest = ''
        if value <= 0:
            raise ValueError
        return qualifier, value, rest

    def __parse_value__(self, time_value: str) -> None:
        """
        Parse specified duration value to fields in self.__fields__

        Parsed values are stored to the __fields__ values in the object.

        Invalid strings, duplicate field names and non-positive durations raise ValueError

        Arguments
        ---------
        time_value: a valid time string as specified in TIME FORMATS section on sshd manual page
        """
        if not time_value:
            raise ValueError('Invalid duration value')
        rest = str(time_value)
        while rest:
            try:
                qualifier, value, rest = self.__parse_duration_field__(rest)
            except ValueError as error:
                raise ValueError(f'Invalid duration string: {time_value}') from error
            if self.__fields__[qualifier] is not None:
                raise ValueError(f'Duplicate qualifier in duration string: {time_value}')
            self.__fields__[qualifier] = value

    @property
    def timedelta(self) -> timedelta:
        """
        Convert data from fields to a datetime.timedelta value

        Returns
        -------
        Value from duration as datetime.timedelta
        """
        duration = timedelta(seconds=0)
        for field, value in self.__fields__.items():
            if value:
                duration += timedelta(seconds=value * SECONDS_MULTIPLIERS[field])
        return duration
