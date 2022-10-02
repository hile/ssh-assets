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
