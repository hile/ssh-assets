"""
Common base command for 'ssh-assets config' subcommands
"""
from ...base import SshAssetsCommand


class AssetsConfigCommand(SshAssetsCommand):
    """
    SSH assets CLI command for commands that process SSH assets configuration
    """
