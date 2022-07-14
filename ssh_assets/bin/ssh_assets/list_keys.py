"""
CLI 'ssh-assets' subcommand 'list-keys'
"""

from ssh_assets.constants import USER_CONFIGURATION_FILE

from ..base import SshAssetsCommand

USAGE = """List configured SSH keys
"""
DESCRIPTION = f"""
This command can be used to list SSH key files configured to the SSH assets
configuration file {USER_CONFIGURATION_FILE}.
"""


class ListKeysCommand(SshAssetsCommand):
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
        for item in self.session.configuration.keys:
            print(item.private_key)
