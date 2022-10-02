"""
Base commands for all SSH assets CLI subcommands
"""
from argparse import ArgumentParser, Namespace
from typing import List

from fnmatch import fnmatch
from pathlib import Path

from cli_toolkit.command import Command

from ..configuration.groups import GroupListConfigurationSection
from ..configuration.keys import SshKeyListConfigurationSection, SshKeyConfiguration
from ..keys.agent import SshAgent
from ..session import SshAssetSession


class SshAssetsCommand(Command):
    """
    Common base class for 'ssh-assets' subcommands
    """
    session = None

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
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

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
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
    def agent(self) -> SshAgent:
        """
        Return SSH agent keys iterator
        """
        return self.session.agent

    @property
    def groups(self) -> GroupListConfigurationSection:
        """
        Return groups configured in the SSH assets configuration file
        """
        return self.session.configuration.groups  # pylint: disable=no-member

    @property
    def keys(self) -> SshKeyListConfigurationSection:
        """
        Return keys configured in the SSH assets configuration file
        """
        return self.session.configuration.keys  # pylint: disable=no-member

    @staticmethod
    def filter_key_groups(keys: List[SshKeyConfiguration],
                          args: Namespace) -> List[SshKeyConfiguration]:
        """
        Return keys included in specified group name mathces in args.group_matches
        """
        def match_groups(groups: List[str], key) -> bool:
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
    def filter_key_names(keys: List[SshKeyConfiguration],
                         args: Namespace) -> List[SshKeyConfiguration]:
        """
        Return keys matching key name list from args.keys
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

    def filter_keys(self, args: Namespace) -> List[SshKeyConfiguration]:
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
        if not keys:
            if not args.groups and not args.keys:
                self.exit(1, 'No keys are configured in the SSH assets configuration file')
            else:
                self.exit(1, 'No keys matching query arguments detected')
        return keys
