"""
Base command for 'ssh-assets keys' subcommands
"""
from argparse import ArgumentParser, Namespace

from ...base import SshAssetsCommand


class SshKeyListCommand(SshAssetsCommand):
    """
    SSH assets CLI command for commands that process SSH keys

    This command subclass takes an optional list of SSH key file paths as argument
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add arguments to the keys subcommand parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            'keys',
            nargs='*',
            help='SSH keys to process (name or path)'
        )
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse specified arguments
        """
        args = super().parse_args(args, namespace)
        return args
