"""
CLI 'ssh-assets config groups'
"""
from argparse import Namespace

from .base import SshKeyGroupsCommand

USAGE = """
List configured key groups
"""

DESCRIPTION = """
"""


class ListGroupsCommand(SshKeyGroupsCommand):
    """
    Subcommand to list SSH assets configuration groups
    """
    name = 'list'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args: Namespace) -> None:
        """
        List the keys in asset configuration file or in the SSH agent
        """
        for group in self.groups:
            self.message(f'{group.expire} {group}')
