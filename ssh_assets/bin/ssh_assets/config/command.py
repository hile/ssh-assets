"""
CLI 'ssh-assets' subcommand container 'config'
"""

from cli_toolkit.command import Command

from ssh_assets.constants import USER_CONFIGURATION_FILE

USAGE = """
Configure ssh-assets tool
"""

DESCRIPTION = f"""
Change the configuration of SSH assets configure in the user configuration file
{USER_CONFIGURATION_FILE}
"""


class ConfigCommand(Command):
    """
    CLI command group 'ssh-assets config'
    """
    name = 'config'
    subcommands = (
    )
    usage = USAGE
    description = DESCRIPTION
