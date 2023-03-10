#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI command 'ssh-assets keys delete'
"""
from argparse import Namespace

from .base import SshKeyCommand

USAGE = """
Delete SSH key from SSH assets configuration

This command does not delete the key file.
"""


class DeleteKeyCommand(SshKeyCommand):
    """
    Subcommand to delete SSH key from the keys configuration
    """
    name = 'delete'
    usage = USAGE

    def run(self, args: Namespace) -> None:
        """
        Run command to delete a key from keys configuration
        """
        key = self.keys.get_key_by_name(args.name)
        if not key:
            self.exit(1, f'Key not found in SSH assets configurion: {args.name}')
        self.message(f'delete key {args.name}')
        self.keys.delete_key(args.name)
