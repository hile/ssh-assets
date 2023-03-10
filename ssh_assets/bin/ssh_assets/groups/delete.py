#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'ssh-assets config groups delete'
"""
from argparse import Namespace

from .base import SshKeyGroupEditCommand

USAGE = """
Delete existing key group from SSH assets configuration
"""

DESCRIPTION = """
"""


class DeleteGroupCommand(SshKeyGroupEditCommand):
    """
    Subcommand to delete SSH assets configuration group
    """
    name = 'delete'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args: Namespace) -> None:
        """
        Delete a key to the configuration
        """
        group = self.groups.get_group_by_name(args.name)
        if not group:
            self.exit(1, f'Group not configured: {args.name}')
        self.groups.delete_group(args.name)
