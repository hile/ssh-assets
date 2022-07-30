"""
CLI 'ssh-assets' subcommand 'list-keys'
"""

from ssh_assets.constants import USER_CONFIGURATION_FILE

from ..base import SshKeysCommand

USAGE = """List SSH keys
"""
DESCRIPTION = f"""
This command can be used to list SSH keys loaded to the agent (default mode) or
SSH keys configured in the SSH assets configuration file.

 User SSH assets configuration file path is {USER_CONFIGURATION_FILE}).
"""


class ListKeysCommand(SshKeysCommand):
    """
    Subcommand to list SSH keys in assets configuration and loaded to the agent
    """
    name = 'list-keys'
    usage = USAGE
    description = DESCRIPTION

    def register_parser_arguments(self, parser):
        """
        Add arguments for listing keys in agent
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '-c', '--configured',
            action='store_true',
            help='List configured SSH keys'
        )
        parser.add_argument(
            '-a', '--available',
            action='store_true',
            help='List configured and available SSH keys'
        )
        return parser

    def list_configured_keys(self, args):
        """
        List SSH keys configred in the SSH assets configuration file
        """
        for key in self.filter_keys(args):
            if args.available and not key.available:
                continue
            self.message(f'{key.name} {key.private_key}')

    # pylint: disable=unused-argument
    def list_ssh_agent_keys(self, args):
        """
        List SSH keys configered to the agent
        """
        for key in self.agent:
            self.message(key)

    def run(self, args):
        """
        List the keys in asset configuration file or in the SSH agent
        """
        if args.configured or args.available:
            return self.list_configured_keys(args)
        return self.list_ssh_agent_keys(args)
