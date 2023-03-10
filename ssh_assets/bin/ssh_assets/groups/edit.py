#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'ssh-assets config groups edit'
"""
from argparse import Namespace

from .base import SshKeyGroupEditCommand

USAGE = """
Edit existing key group in SSH assets configuration
"""

DESCRIPTION = """
"""


class EditGroupCommand(SshKeyGroupEditCommand):
    """
    Subcommand to edit SSH assets configuration group
    """
    name = 'edit'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args: Namespace) -> None:
        """
        Edit a key to the configuration
        """
        group = self.groups.get_group_by_name(args.name)
        if not group:
            self.exit(1, f'Group not configured: {args.name}')
        self.groups.configure_group(args.name, **self.get_update_kwargs(args))
