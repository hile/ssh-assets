"""
CLI 'ssh-assets' subcommand container 'keys'
"""

from cli_toolkit.command import Command

from ssh_assets.constants import USER_CONFIGURATION_FILE

from .add import AddKeyCommand
from .edit import EditKeyCommand
from .list import ListKeysCommand
from .load import LoadKeysCommand
from .unload import UnLoadKeysCommand

USAGE = """
List, load and unload SSH keys
"""

DESCRIPTION = f"""
List, load and unload SSH keys configured to user ssh assets configuration file
{USER_CONFIGURATION_FILE}
"""


class KeysCommand(Command):
    """
    CLI command group 'ssh-assets keys'
    """
    name = 'keys'
    subcommands = (
        ListKeysCommand,
        AddKeyCommand,
        EditKeyCommand,
        LoadKeysCommand,
        UnLoadKeysCommand,
    )
    usage = USAGE
    description = DESCRIPTION
