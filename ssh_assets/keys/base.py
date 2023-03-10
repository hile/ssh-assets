#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Base classes for SSH key file processing
"""
import re

from pathlib import Path
from typing import Any, Callable, List

from ..base import RichComparisonObject
from ..exceptions import SSHKeyError

from .constants import (
    KeyHashAlgorithm,
    SshKeyType,
    DEFAULT_KEY_HASH_ALGORITHM,
)

RE_KEY_ATTRIBUTES = re.compile(
    r'^(?P<bits>\d+)\s+'
    r'(?P<hash_algorithm>[A-Z0-9]+):(?P<hash>[^\s]+)\s+'
    r'(?P<comment>.*)\s+'
    r'\((?P<key_type>[^\s]+)\)$'
)
KEY_COMPARE_ATTRIBUTES = (
    'bits',
    'key_type',
    'hash_algorithm',
    'hash',
)
KEY_INTEGER_ATTRIBUTES = (
    'bits',
)
KEY_STRING_ATTRIBUTES = (
    'comment',
)


class SSHKeyLoader(RichComparisonObject):
    """
    SSH key base class

    Base class for SSH private and public keys
    """
    hash_algorithm: str
    __key_attributes__: dict

    __compare_attributes__ = KEY_COMPARE_ATTRIBUTES
    __identity_attributes__ = ()

    def __init__(self, hash_algorithm: str = DEFAULT_KEY_HASH_ALGORITHM) -> None:
        if not isinstance(hash_algorithm, KeyHashAlgorithm):
            raise SSHKeyError('SSH key hash algorithm must be an KeyHashAlgorithm enum value')
        self.hash_algorithm = hash_algorithm
        self.__key_attributes__ = {}
        self.path = None

    def __compare__(self, operator: Callable, default: bool, other: Any) -> bool:
        """
        Common compare method for sorting
        """
        if self.path is not None and isinstance(other, Path):
            return operator(self.path, other)
        if isinstance(other, str):
            return operator(self.hash, other)
        return super().__compare__(operator, default, other)

    def __eq__(self, other) -> bool:
        if self.path is not None and isinstance(other, Path):
            return self.path == other
        if isinstance(other, str):
            return self.hash == other
        return super().__eq__(other)

    def __load_key_attributes__(self) -> None:
        """
        Load key attributes to the class

        This method must be overridden in the key child class
        """
        raise NotImplementedError('__load_key_attributes__() must be implemented in child class')

    def __parse_key_info_line__(self, line: str) -> None:
        """
        Parse key attributes from key info line
        """
        match = RE_KEY_ATTRIBUTES.match(line)
        if not match:
            raise SSHKeyError(f'Unexpected output: {line}')

        self.__key_attributes__ = match.groupdict()
        for attr in KEY_STRING_ATTRIBUTES:
            self.__key_attributes__[attr] = str(self.__key_attributes__[attr])
        for attr in KEY_INTEGER_ATTRIBUTES:
            self.__key_attributes__[attr] = int(self.__key_attributes__[attr])

    def __get_key_attribute__(self, attr: str) -> str:
        """
        Get key attribute for key.

        Key data is cached to __key_attributes__ after first load and not loaded again.
        """
        if not self.__key_attributes__:
            self.__load_key_attributes__()
        try:
            return self.__key_attributes__[attr]
        except KeyError as error:
            raise SSHKeyError(f'Unexpected SSH key attribute: {attr}') from error

    @property
    def identity_parameters(self) -> List[str]:
        """
        Return identity parameter values that can be used to match this key
        """
        parameters = []
        for attr in self.__identity_attributes__:
            parameters.append(str(getattr(self, attr, '')))
        return parameters

    @property
    def bits(self) -> int:
        """
        Return key bits as integer
        """
        return self.__get_key_attribute__('bits')

    @property
    def hash(self) -> str:
        """
        Return key checksum hash as string
        """
        return self.__get_key_attribute__('hash')

    @property
    def key_type(self) -> str:
        """
        Return key type as string
        """
        return SshKeyType(self.__get_key_attribute__('key_type'))

    @property
    def comment(self) -> str:
        """
        Return key comment as string
        """
        return self.__get_key_attribute__('comment')
