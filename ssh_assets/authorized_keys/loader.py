#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Class to load OpenSSH authorized keys files
"""
from pathlib import Path

from sys_toolkit.collection import CachedMutableSequence

from ..exceptions import SSHKeyError
from .constants import DEFAULT_AUTHORIZED_KEYS_FILE
from .public_key import PublicKey


class AuthorizedKeys(CachedMutableSequence):
    """
    List of OpenSSH authorized keys items
    """
    path: Path

    def __init__(self, path: str = DEFAULT_AUTHORIZED_KEYS_FILE) -> None:
        super().__init__()
        self.path = Path(path).expanduser().resolve()

    def update(self) -> None:
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
                self.__items__.append(PublicKey(line))
        except OSError as error:
            raise SSHKeyError(
                f'Error loading SSH authorized keys list from {self.path}: {error}'
            ) from error

        self.__finish_update__()
