"""
CLI 'ssh-assets config groups'
"""

from ..base import AssetsConfigCommand

USAGE = """
List configured key groups
"""

DESCRIPTION = """
"""


class ListGroupsCommand(AssetsConfigCommand):
    """
    Subcommand to list SSH assets configuration groups
    """
    name = 'list'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args):
        """
        List the keys in asset configuration file or in the SSH agent
        """
        for group in self.groups:
            self.message(f'{group.expire} {group}')
