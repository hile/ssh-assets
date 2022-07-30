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

    def register_parser_arguments(self, parser):
        """
        Add arguments to the keys subcommand parser
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '-g', '--groups',
            action='append',
            help='Asset configuration groups to match'
        )
        return parser

    def parse_args(self, args=None, namespace=None):
        """
        Parse arguments and add reference to the session
        """
        args = super().parse_args(args, namespace)
        self.session = SshAssetSession()
        if args.groups:
            args.groups = [var for arg in args.groups for var in arg.split(',')]
            args.group_matches = []
            for name in args.groups:
                group = self.groups.get_group_by_name(name)
                if group:
                    args.group_matches.append(group)
        return args

    @property
    def groups(self):
        """
        Return groups configured in the SSH assets configuration file
        """
        return self.session.configuration.groups  # pylint: disable=no-member

    @property
    def keys(self):
        """
        Return keys configured in the SSH assets configuration file
        """
        return self.session.configuration.keys  # pylint: disable=no-member
