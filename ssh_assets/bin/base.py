"""
Base commands for all SSH assets CLI subcommands
"""

from cli_toolkit.command import Command

from ..session import SshAssetSession


class SshAssetsCommand(Command):
    """
    Common base class for 'ssh-assets' subcommands
    """
    session = None

    def parse_args(self, args=None, namespace=None):
        """
        Parse arguments and add reference to the session
        """
        args = super().parse_args(args, namespace)
        self.session = SshAssetSession()
        return args
