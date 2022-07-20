"""
SSH client configuration token strign processing
"""

from enum import Enum

from .base import TokenStringValidator


class ClientConfigToken(Enum):
    """
    SSH client configuration string token
    """
    LOCAL_HOSTNAME = '%L'
    LOCAL_HOSTNAME_FQDN = '%l'
    LOCAL_USER_ID = '%i'
    LOCAL_USERNAME = '%u'
    LOCAL_USER_HOME_DIRECTORY = '%d'
    LOCAL_TUNTAP_INTERFACE = '%T'

    REMOTE_HOSTNAME_ORIGINAL = '%n'
    REMOTE_HOST_ALIAS = '%k'
    REMOTE_HOSTNAME = '%h'
    HOST_KEY_BASE64 = '%K'
    REMOTE_PORT = '%p'
    REMOTE_USERNAME = '%r'
    CONNECTION_STRING_HASH = '%C'
    KNOWN_HOSTS_LOOKUP = '%H'
    KNOWN_HOSTS_COMMAND_REASON = '%I'
    SERVER_HOST_KEY_TYPE = '%t'
    SERVER_HOST_KEY_FINGERPRINT = '%f'
    LITERAL_PERCENT = '%%'


# pylint: disable=too-few-public-methods
class ClientFilePathTokenStringValidator(TokenStringValidator):
    """
    Generic token string for filesystem paths for SSH client configuration tokens
    """
    __suppported_tokens__ = (
        ClientConfigToken.LITERAL_PERCENT,
        ClientConfigToken.CONNECTION_STRING_HASH,
        ClientConfigToken.LOCAL_HOSTNAME_FQDN,
        ClientConfigToken.LOCAL_HOSTNAME,
        ClientConfigToken.LOCAL_USER_HOME_DIRECTORY,
        ClientConfigToken.LOCAL_USER_ID,
        ClientConfigToken.LOCAL_USERNAME,
        ClientConfigToken.REMOTE_HOST_ALIAS,
        ClientConfigToken.REMOTE_HOST_ALIAS,
        ClientConfigToken.REMOTE_HOSTNAME_ORIGINAL,
        ClientConfigToken.REMOTE_PORT,
        ClientConfigToken.REMOTE_USERNAME,
    )


# pylint: disable=too-few-public-methods
class CertificateFile(ClientFilePathTokenStringValidator):
    """
    Token string for CertificateFile ssh client configuration option
    """
    __option__ = 'CertificateFile'


# pylint: disable=too-few-public-methods
class ControlPath(ClientFilePathTokenStringValidator):
    """
    Token string for ControlPath ssh client configuration option
    """
    __option__ = 'ControlPath'


# pylint: disable=too-few-public-methods
class IdentityAgent(ClientFilePathTokenStringValidator):
    """
    Token string for IdentityAgent ssh client configuration option
    """
    __option__ = 'IdentityAgent'


# pylint: disable=too-few-public-methods
class IdentityFile(ClientFilePathTokenStringValidator):
    """
    Token string for IdentityFile ssh client configuration option
    """
    __option__ = 'IdentityFile'


# pylint: disable=too-few-public-methods
class LocalForward(ClientFilePathTokenStringValidator):
    """
    Token string for LocalForward ssh client configuration option
    """
    __option__ = 'LocalForward'


# pylint: disable=too-few-public-methods
class Match(ClientFilePathTokenStringValidator):
    """
    Token string for Match ssh client configuration option
    """
    __option__ = 'Match'


# pylint: disable=too-few-public-methods
class Exec(ClientFilePathTokenStringValidator):
    """
    Token string for exec ssh client configuration option
    """
    __option__ = 'exec'


# pylint: disable=too-few-public-methods
class RemoteCommand(ClientFilePathTokenStringValidator):
    """
    Token string for RemoteCommand ssh client configuration option
    """
    __option__ = 'RemoteCommand'


# pylint: disable=too-few-public-methods
class RemoteForward(ClientFilePathTokenStringValidator):
    """
    Token string for RemoteForward ssh client configuration option
    """
    __option__ = 'RemoteForward'


# pylint: disable=too-few-public-methods
class UserKnownHostsFile(ClientFilePathTokenStringValidator):
    """
    Token string for UserKnownHostsFile ssh client configuration option
    """
    __option__ = 'UserKnownHostsFile'


# pylint: disable=too-few-public-methods
class KnownHostsCommand(TokenStringValidator):
    """
    Token string for KnownHostsCommand ssh client option
    """
    __option__ = 'KnownHostsCommand'
    __suppported_tokens__ = (
        ClientConfigToken.LITERAL_PERCENT,
        ClientConfigToken.CONNECTION_STRING_HASH,
        ClientConfigToken.LOCAL_HOSTNAME_FQDN,
        ClientConfigToken.LOCAL_HOSTNAME,
        ClientConfigToken.LOCAL_USER_HOME_DIRECTORY,
        ClientConfigToken.LOCAL_USER_ID,
        ClientConfigToken.LOCAL_USERNAME,
        ClientConfigToken.REMOTE_HOST_ALIAS,
        ClientConfigToken.REMOTE_HOST_ALIAS,
        ClientConfigToken.REMOTE_HOSTNAME_ORIGINAL,
        ClientConfigToken.REMOTE_PORT,
        ClientConfigToken.REMOTE_USERNAME,
        ClientConfigToken.KNOWN_HOSTS_LOOKUP,
        ClientConfigToken.KNOWN_HOSTS_COMMAND_REASON,
        ClientConfigToken.HOST_KEY_BASE64,
        ClientConfigToken.SERVER_HOST_KEY_TYPE,
        ClientConfigToken.SERVER_HOST_KEY_FINGERPRINT,
    )


# pylint: disable=too-few-public-methods
class ProxyCommand(TokenStringValidator):
    """
    Token string for ProxyCommand ssh client configuration option
    """
    __option__ = 'ProxyCommand'
    __suppported_tokens__ = (
        ClientConfigToken.LITERAL_PERCENT,
        ClientConfigToken.REMOTE_HOSTNAME,
        ClientConfigToken.REMOTE_HOSTNAME_ORIGINAL,
        ClientConfigToken.REMOTE_PORT,
        ClientConfigToken.REMOTE_USERNAME,
    )


# pylint: disable=too-few-public-methods
class LocalCommand(TokenStringValidator):
    """
    Token string for LocalCommand ssh client configuration option
    """
    __option__ = 'LocalCommand'
    __suppported_tokens__ = tuple(list(ClientConfigToken))


# pylint: disable=too-few-public-methods
class Hostname(TokenStringValidator):
    """
    Token string for Hostname ssh client configuration option
    """
    __option__ = 'Hostname'
    __suppported_tokens__ = (
        ClientConfigToken.REMOTE_HOSTNAME,
    )


CLIENT_CONFIG_TOKEN_STRING_CLASSES = (
    CertificateFile,
    ControlPath,
    Exec,
    Hostname,
    IdentityAgent,
    IdentityFile,
    KnownHostsCommand,
    LocalCommand,
    LocalForward,
    Match,
    ProxyCommand,
    RemoteCommand,
    RemoteForward,
    UserKnownHostsFile,
)
