#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
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


class SshKeyCommand(SshAssetsCommand):
    """
    SSH assets CLI command for commands that access a single key
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add common arguments for SSH key edit command
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument('name', help='SSH key name in assets configuration')
        return parser


class SshKeyEditCommand(SshKeyCommand):
    """
    SSH assets CLI command for command that adds or edits a single key
    """
    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register the optional arguments for adding or editing a key
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument('-a', '--autoload', action='store_true', help='Enable key automatically')
        parser.add_argument('-n', '--no-autoload', action='store_true', help='Disable key automatically')
        parser.add_argument('-e', '--expire', help='Key expiration time')
        parser.add_argument('-E', '--no-expire', action='store_true', help='Delete key expiration time')
        parser.add_argument('--path', help='Path to the key file')
        return parser

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse args and check for conflicting values
        """
        args = super().parse_args(args, namespace)
        if args.autoload and args.no_autoload:
            self.exit(1, 'Conflicting arguments --autoload and --no-autoload')
        if args.expire and args.no_expire:
            self.exit(1, 'Conflicting arguments --expire and --no-expire')
        return args

    def get_update_kwargs(self, args: Namespace) -> dict:
        """
        Get kwargs for configure_key method based on command line arguments
        """
        kwargs = {}
        if args.autoload:
            kwargs['autoload'] = True
        if args.no_autoload:
            kwargs['autoload'] = False
        if args.expire:
            kwargs['expire'] = args.expire
        if args.path:
            kwargs['path'] = args.path
        return kwargs
