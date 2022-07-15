"""
Base commands for all SSH assets CLI subcommands
"""

from fnmatch import fnmatch
from pathlib import Path

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


class SshKeysCommand(SshAssetsCommand):
    """
    SSH assets CLI command for commands that process SSH keys

    This command subclass takes an optional list of SSH key file paths as argument
    """
    def register_parser_arguments(self, parser):
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

    def filter_keys(self, args):
        """
        Return keys matching specified arguments
        """
        def match_keys(patterns, name):
            """
            Match specified key name to list of strings
            """
            for pattern in patterns:
                if fnmatch(name, pattern):
                    return True
            return False

        configured_keys = self.session.configuration.keys  # pylint: disable=no-member
        if not args.keys:
            return configured_keys

        paths = [Path(arg).expanduser().resolve() for arg in args.keys]
        matching_keys = []
        for key in configured_keys:
            if match_keys(args.keys, key.name) or key.path.resolve() in paths:
                matching_keys.append(key)
        return matching_keys
