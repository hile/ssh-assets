"""
Base command for 'ssh-assets groups' subcommands
"""
from argparse import ArgumentParser, Namespace

from ...base import SshAssetsCommand


class SshKeyGroupsCommand(SshAssetsCommand):
    """
    SSH assets CLI command for commands that process SSH key groups in asset
    configuration file

    This command subclass takes an optional list of SSH group names as argument
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add arguments to the group names to subcommand parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            'groups',
            nargs='*',
            help='SSH key group names to process'
        )
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse specified arguments
        """
        args = super().parse_args(args, namespace)
        return args
