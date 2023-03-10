#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'ssh-assets config groups add'
"""
from argparse import Namespace

from .base import SshKeyGroupEditCommand

USAGE = """
Add a key group to SSH assets configuration
"""

DESCRIPTION = """
"""


class AddGroupCommand(SshKeyGroupEditCommand):
    """
    Subcommand to add SSH assets keys configuration group
    """
    name = 'add'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args: Namespace) -> None:
        """
        Add a key to the configuration
        """
        group = self.groups.get_group_by_name(args.name)
        if group:
            self.exit(1, f'Group already configured: {args.name}')
        self.groups.configure_group(args.name, **self.get_update_kwargs(args))

        for group in self.groups:
            self.message(f'{group.expire} {group}')
