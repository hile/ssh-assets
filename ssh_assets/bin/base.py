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
            '-g', '--groups',
            action='append',
            help='Asset configuration groups to match'
        )
        parser.add_argument(
            'keys',
            nargs='*',
            help='SSH keys to process (name or path)'
        )
        return parser

    def parse_args(self, args=None, namespace=None):
        """
        Parse specified arguments
        """
        args = super().parse_args(args, namespace)
        if args.groups:
            args.groups = [var for arg in args.groups for var in arg.split(',')]
            args.group_matches = []
            for name in args.groups:
                group = self.groups.get_group(name)
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

    @staticmethod
    def filter_key_groups(keys, args):
        """
        Return keys matching specified
        """
        def match_groups(groups, key):
            for group in groups:
                if key.name in group.keys:
                    return True
            return False

        if not args.groups:
            return keys

        matching_keys = []
        for key in keys:
            if match_groups(args.group_matches, key):
                matching_keys.append(key)
        return matching_keys

    @staticmethod
    def filter_key_names(keys, args):
        """
        Return keys matching key name list
        """
        def match_keys(patterns, name):
            """
            Match specified key name to list of strings
            """
            for pattern in patterns:
                if fnmatch(name, pattern):
                    return True
            return False

        if not args.keys:
            return keys

        paths = [Path(arg).expanduser().resolve() for arg in args.keys]
        matching_keys = []
        for key in keys:
            if match_keys(args.keys, key.name) or key.path.resolve() in paths:
                matching_keys.append(key)
        return matching_keys

    def filter_keys(self, args):
        """
        Return keys matching specified arguments
        """
        filter_methdos = (
            self.filter_key_groups,
            self.filter_key_names,
        )
        keys = self.keys
        for method in filter_methdos:
            keys = method(keys, args)
        return keys
