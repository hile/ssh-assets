#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI command 'ssh-assets keys add'
"""
from argparse import Namespace

from .base import SshKeyEditCommand

USAGE = """
Add SSH key to SSH assets configuration
"""


class AddKeyCommand(SshKeyEditCommand):
    """
    Subcommand to add SSH key to the configuration
    """
    name = 'add'
    usage = USAGE

    def run(self, args: Namespace) -> None:
        """
        Run command to add a key to keys configuration
        """
        key = self.keys.get_key_by_name(args.name)
        if key:
            self.exit(1, f'Key already configured in SSH assets configurion: {args.name}')
        self.message(f'add key {args.name}')
        self.keys.configure_key(args.name, **self.get_update_kwargs(args))
