"""
CLI command 'ssh-assets keys add'
"""
from argparse import Namespace

from .base import SshKeyEditCommand

USAGE = """
Edit existing SSH key in SSH assets configuration
"""


class EditKeyCommand(SshKeyEditCommand):
    """
    Subcommand to add SSH key to the configuration
    """
    name = 'edit'
    usage = USAGE

    def run(self, args: Namespace) -> None:
        """
        Run command to edit a key in keys configuration
        """
        key = self.keys.get_key_by_name(args.name)
        if not key:
            self.exit(1, f'Key not found in SSH assets configurion: {args.name}')
        self.message(f'edit key {key}')
        self.keys.configure_key(args.name, **self.get_update_kwargs(args))
