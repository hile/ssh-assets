"""
CLI 'ssh-assets config' subcommand container 'groups'
"""

from cli_toolkit.command import Command

from .list import ListGroupsCommand

USAGE = """
Configure ssh-assets configuration groups
"""

DESCRIPTION = """
Change the configuration of SSH assets configuration groups
"""


class GroupsCommand(Command):
    """
    CLI command group 'ssh-assets groups'
    """
    name = 'groups'
    subcommands = (
        ListGroupsCommand,
    )
    usage = USAGE
    description = DESCRIPTION
