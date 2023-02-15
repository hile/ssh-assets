"""
CLI 'ssh-assets' subcommand 'unload-keys'
"""
from argparse import ArgumentParser, Namespace

from ssh_assets.constants import USER_CONFIGURATION_FILE

from .base import SshKeyListCommand

USAGE = f"""Unload configured SSH keys from agent

This command can be used to unload SSH keys configured in the SSH assets
configuration file {USER_CONFIGURATION_FILE} to SSH user's keyring. The
keys are specified by key name in key configuration, not by key path.

If --all is not specified, all keys in the agent are removed: this is done by
normal 'ssh-add -D' call.
"""


class UnLoadKeysCommand(SshKeyListCommand):
    """
    Subcommand to unload SSH keys to agent
    """
    name = 'unload'
    usage = USAGE

    def register_parser_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """
        Register various parser arguments
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '--all',
            action='store_true',
            help='UnLoad all keys from SSH agent'
        )
        return parser

    # pylint: disable=unused-argument
    def run(self, args: Namespace) -> None:
        """
        UnLoad SSH keys from the SSH agent
        """
        if not args.groups and not args.keys:
            self.session.agent.unload_keys_from_agent(unload_all_keys=True)
        else:
            self.session.agent.unload_keys_from_agent(
                keys=self.get_filter_set(args).keys,
                unload_all_keys=False
            )
