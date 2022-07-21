"""
CLI 'ssh-assets' subcommand 'list-keys'
"""

from ssh_assets.constants import USER_CONFIGURATION_FILE

from ..base import SshKeysCommand

USAGE = """List configured SSH keys
"""
DESCRIPTION = f"""
This command can be used to list SSH key files configured to the SSH assets
configuration file {USER_CONFIGURATION_FILE}.
"""


class ListKeysCommand(SshKeysCommand):
    """
    Subcommand to list configured SSH keys
    """
    name = 'list-keys'
    usage = USAGE
    description = DESCRIPTION

    def run(self, args):
        """
        List the keys in asset configuration file
        """
        for item in self.filter_keys(args):
            self.message(f'{item.name} {item.private_key}')
