"""
CLI 'ssh-assets groups list'
"""
from argparse import Namespace

from .base import SshKeyGroupListCommand

USAGE = """
List configured key groups
"""

DESCRIPTION = """
"""


class ListGroupsCommand(SshKeyGroupListCommand):
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
