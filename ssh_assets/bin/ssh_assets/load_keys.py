"""
CLI 'ssh-assets' subcommand 'load-keys'
"""

from ..base import SshAssetsCommand


class LoadKeysCommand(SshAssetsCommand):
    """
    Subcommand to load SSH keys to agent
    """
    name = 'load-keys'

    def register_parser_arguments(self, parser):
        """
        Register various parser arguments
        """
        parser.add_argument(
            '--all',
            action='store_true',
            help='Load all configured keys ignoring autoload flag'
        )
        return parser

    # pylint: disable=unused-argument
    def run(self, args, namespace=None):
        """
        Load SSH keys to the SSH agent
        """
        self.session.load_available_keys(load_all_keys=args.all)
