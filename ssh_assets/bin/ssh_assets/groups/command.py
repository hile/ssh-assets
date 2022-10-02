"""
CLI 'ssh-assets groups' command group
"""

from cli_toolkit.command import Command

from .add import AddGroupCommand
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
        EditGroupCommand,
    )
    usage = USAGE
    description = DESCRIPTION
