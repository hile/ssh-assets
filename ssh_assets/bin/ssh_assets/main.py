"""
Command line tool 'ssh-assets'
"""

from cli_toolkit.script import Script

from .load_keys import LoadKeysCommand


class SshAssetsScript(Script):
    """
    CLI command 'ssh-assets'
    """
    subcommands = (
        LoadKeysCommand,
    )


def main():
    """
    Main CLI entrypoint for the ssh-assets command
    """
    SshAssetsScript().run()
