"""
Command line tool 'ssh-assets'
"""

from cli_toolkit.script import Script

from .list_keys import ListKeysCommand
from .load_keys import LoadKeysCommand
from .unload_keys import UnLoadKeysCommand

USAGE = """SSH key and configuration file assets utility

"""
DESCRIPTION = """
This command can be used to manage more complicated SSH key arrangement, like loading
and using different keys for different tasks from the SSH agent.
"""


class SshAssetsScript(Script):
    """
    CLI command 'ssh-assets'
    """
    usage = USAGE
    description = DESCRIPTION
    subcommands = (
        ListKeysCommand,
        LoadKeysCommand,
        UnLoadKeysCommand,
    )


def main():
    """
    Main CLI entrypoint for the ssh-assets command
    """
    SshAssetsScript().run()
