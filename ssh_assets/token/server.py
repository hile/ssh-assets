"""
SSH server configuration token strign processing
"""

from enum import Enum

from .base import TokenStringValidator


# pylint: disable=too-few-public-methods
class ServerConfigToken(Enum):
    """
    SSH server configuration string token
    """
    HOME = '%h'
    KEY_ID = '%i'
    USER_ID = '%U'
    USERNAME = '%u'
    CA_KEY_FINGERPRINT = '%F'
    CA_KEY_BASE64 = '%K'
    CA_KEY_TYPE = '%T'
    CERTIFICATE_SERIAL_NUMBER = '%s'
    CERTIFICATE_FINGERPRINT = '%f'
    CERTIFICATE_BASE64 = '%k'
    CERTIFICATE_TYPE = '%t'
    ROUTING_DOMAIN = '%D'
    LITERAL_PERCENT = '%%'


# pylint: disable=too-few-public-methods
class ServerFilePathTokenStringValidator(TokenStringValidator):
    """
    Generic token string for filesystem paths for SSH server configuration tokens
    """
    __suppported_tokens__ = (
        ServerConfigToken.HOME,
        ServerConfigToken.USER_ID,
        ServerConfigToken.USERNAME,
        ServerConfigToken.LITERAL_PERCENT,
    )


# pylint: disable=too-few-public-methods
class AuthorizedKeysCommand(TokenStringValidator):
    """
    Token string for AuthorizedPrincipalsCommand sshd option
    """
    __suppported_tokens__ = (
        ServerConfigToken.HOME,
        ServerConfigToken.USER_ID,
        ServerConfigToken.USERNAME,
        ServerConfigToken.CERTIFICATE_FINGERPRINT,
        ServerConfigToken.CERTIFICATE_BASE64,
        ServerConfigToken.CERTIFICATE_TYPE,
        ServerConfigToken.LITERAL_PERCENT,
    )


# pylint: disable=too-few-public-methods
class AuthorizedKeysFile(ServerFilePathTokenStringValidator):
    """
    Token string for AuthorizedKeysFile sshd option
    """


# pylint: disable=too-few-public-methods
class AuthorizedPrincipalsCommand(TokenStringValidator):
    """
    Token string for AuthorizedPrincipalsCommand sshd option
    """
    __suppported_tokens__ = (
        ServerConfigToken.HOME,
        ServerConfigToken.KEY_ID,
        ServerConfigToken.USER_ID,
        ServerConfigToken.USERNAME,
        ServerConfigToken.CA_KEY_FINGERPRINT,
        ServerConfigToken.CA_KEY_BASE64,
        ServerConfigToken.CA_KEY_TYPE,
        ServerConfigToken.CERTIFICATE_SERIAL_NUMBER,
        ServerConfigToken.CERTIFICATE_FINGERPRINT,
        ServerConfigToken.CERTIFICATE_BASE64,
        ServerConfigToken.CERTIFICATE_TYPE,
        ServerConfigToken.LITERAL_PERCENT,
    )


# pylint: disable=too-few-public-methods
class AuthorizedPrincipalsFile(ServerFilePathTokenStringValidator):
    """
    Token string for parsing authorized principals file path
    """


# pylint: disable=too-few-public-methods
class ChrootDirectory(ServerFilePathTokenStringValidator):
    """
    Token string for ChrootDirectory sshd option
    """


SERVER_CONFIG_TOKEN_STRING_CLASSES = (
    AuthorizedKeysCommand,
    AuthorizedKeysFile,
    AuthorizedPrincipalsCommand,
    AuthorizedPrincipalsFile,
    ChrootDirectory,
)
