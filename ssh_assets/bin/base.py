#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Base commands for all SSH assets CLI subcommands
"""
from argparse import ArgumentParser, Namespace

from cli_toolkit.command import Command

from ..configuration.groups import GroupListConfigurationSection
from ..configuration.keys import SshKeyListConfigurationSection
from ..constants import NO_KEYS_CONFIGURED, NO_KEYS_MATCH
from ..duration import Duration
from ..keys.agent import SshAgent
from ..keys.filter_set import SshKeyFilterSet
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

        if getattr(args, 'expire', None) is not None:
            try:
                args.expire = Duration(args.expire)
            except ValueError:
                self.exit(1, f'Invalid key expiration value: {args.expire}')

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

    def get_filter_set(self, args: Namespace) -> SshKeyFilterSet:
        """
        Return keys matching specified arguments
        """
        filter_set = self.session.key_filter_set
        if 'keys' in args and args.keys:
            filter_set = filter_set.filter_names(args.keys)

        if 'groups' in args and args.groups:
            filter_set = filter_set.filter_groups(args.groups)

        if 'available' in args and args.available:
            filter_set = filter_set.filter_available(args.available)

        if not filter_set.keys:
            if not args.groups and not args.keys:
                self.exit(1, NO_KEYS_CONFIGURED)
            else:
                self.exit(1, NO_KEYS_MATCH)

        return filter_set
