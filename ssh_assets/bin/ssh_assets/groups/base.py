"""
Base command for 'ssh-assets groups' subcommands
"""
from argparse import ArgumentParser, Namespace

from ...base import SshAssetsCommand


class SshKeyGroupListCommand(SshAssetsCommand):
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


class SshKeyGroupCommand(SshAssetsCommand):
    """
    Base command linked for processing a single group item
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add arguments to the group names to subcommand parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument('name', help='SSH key group name')
        return parser


class SshKeyGroupEditCommand(SshKeyGroupCommand):
    """
    Base command linked for editing a single group
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add arguments to the group names to subcommand parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument('-e', '--expire', help='Group expiration')
        parser.add_argument('-E', '--no-expire', action='store_true', help='Delete key expiration time')
        parser.add_argument('-k', '--keys', action='append', help='Keys in group')
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse group editor arguments
        """
        args = super().parse_args(args, namespace)
        if args.keys:
            args.keys = [value.strip() for arg in args.keys for value in arg.split(',')]
        if args.expire and args.no_expire:
            self.exit(1, 'Conflicting arguments --expire and --no-expire')
        return args

    def get_update_kwargs(self, args: Namespace) -> dict:
        """
        Get kwargs for configure_key method based on command line arguments
        """
        kwargs = {}
        if args.expire:
            kwargs['expire'] = args.expire
        if args.no_expire:
            kwargs['expire'] = None
        if args.keys:
            kwargs['keys'] = args.keys
        return kwargs
