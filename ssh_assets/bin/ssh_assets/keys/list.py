#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'ssh-assets keys list'
"""
import itertools
from argparse import ArgumentParser, Namespace

from ssh_assets.constants import USER_CONFIGURATION_FILE

from .base import SshKeyListCommand

USAGE = """List SSH keys
"""
DESCRIPTION = f"""
This command can be used to list SSH keys loaded to the agent (default mode) or
SSH keys configured in the SSH assets configuration file.

 User SSH assets configuration file path is {USER_CONFIGURATION_FILE}).
"""


class ListKeysCommand(SshKeyListCommand):
    """
    Subcommand to list SSH keys in assets configuration and loaded to the agent
    """
    name = 'list'
    usage = USAGE
    description = DESCRIPTION

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Add arguments for listing keys in agent
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '--autocomplete',
            action='store_true',
            help='Show each key details as autocomplete parameters'
        )
        parser.add_argument(
            '-a', '--available',
            action='store_true',
            help='List available SSH keys'
        )

        parser.add_argument(
            '-l', '--loaded',
            action='store_true',
            help='List loaded SSH keys'
        )
        return parser

    def list_agent_key_identity_parameters(self) -> None:
        """
        List autocomplete parameters for keys loaded in ssh-agent
        """
        parameters = sorted(set(itertools.chain(*[key.identity_parameters for key in self.agent])))
        for parameter in parameters:
            self.message(parameter)

    def list_key_identity_parameters(self, keys) -> None:
        """
        List autocomplete parameters for keys from ssh-assets configuration
        """
        parameters = sorted(set(itertools.chain(*[key.identity_parameters for key in keys])))
        for parameter in parameters:
            self.message(parameter)

    def list_agent_keys(self, args: Namespace) -> None:
        """
        List keys loaded to ssh agent
        """
        if args.autocomplete:
            self.list_agent_key_identity_parameters()
        else:
            for key in self.agent:
                self.message(key)

    def list_keys(self, args: Namespace) -> None:
        """
        List keys in ssh-assets configuration
        """
        keys = self.get_filter_set(args).keys
        if args.autocomplete:
            self.list_key_identity_parameters(keys)
        else:
            for key in keys:
                self.message(f'{key.name} {key.private_key}')

    def run(self, args: Namespace) -> None:
        """
        List the keys in asset configuration file or in the SSH agent
        """
        if args.loaded:
            return self.list_agent_keys(args)
        return self.list_keys(args)
