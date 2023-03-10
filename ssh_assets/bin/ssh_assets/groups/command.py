#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'ssh-assets groups' command group
"""
from cli_toolkit.command import Command

from .add import AddGroupCommand
from .delete import DeleteGroupCommand
from .edit import EditGroupCommand
from .list import ListGroupsCommand

USAGE = """
Configure ssh-assets configured key groups
"""

DESCRIPTION = """
Change the configuration of SSH assets key configuration groups
"""


class GroupsCommand(Command):
    """
    CLI command group 'ssh-assets groups'
    """
    name = 'groups'
    subcommands = (
        ListGroupsCommand,
        AddGroupCommand,
        DeleteGroupCommand,
        EditGroupCommand,
    )
    usage = USAGE
    description = DESCRIPTION
