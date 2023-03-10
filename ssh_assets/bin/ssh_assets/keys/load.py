#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI command 'ssh-assets keys load'
"""
from argparse import ArgumentParser, Namespace

from ssh_assets.constants import USER_CONFIGURATION_FILE

from .base import SshKeyListCommand

USAGE = f"""Load configured SSH keys

This command can be used to load SSH keys configured in the SSH assets
configuration file {USER_CONFIGURATION_FILE} to SSH user's keyring.

If --all is not specified, keys configured to autoload are loaded. If --all
is specified, all keys in the configuration file are loaded.

Unlike normal ssh-agent, the loaded keys in keyring are detected by the key
checksum and are skipped if the key was already loaded to the ssh agent.
"""


class LoadKeysCommand(SshKeyListCommand):
    """
    Subcommand to load SSH keys to agent
    """
    name = 'load'
    usage = USAGE

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register various parser arguments
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '--all',
            action='store_true',
            help='Load all configured keys ignoring autoload flag'
        )
        return parser

    # pylint: disable=unused-argument
    def run(self, args: Namespace) -> None:
        """
        Load SSH keys to the SSH agent
        """
        if not args.groups and not args.keys:
            self.session.agent.load_keys_to_agent(load_all_keys=args.all)
        else:
            self.session.agent.load_keys_to_agent(
                keys=self.get_filter_set(args).keys,
                load_all_keys=True
            )
