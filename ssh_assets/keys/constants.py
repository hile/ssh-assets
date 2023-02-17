"""
Constants used in SSH key processing
"""

from enum import Enum


class KeyHashAlgorithm(Enum):
    """
    SSH key hash algorithms
    """
    MD5 = 'md5'
    SHA_256 = 'sha256'


class SshKeyType(Enum):
    """
    Valid SSH key types
    """
    DSA = 'DSA'
    DSS = 'DSS'
    ECDSA = 'ECDSA'
    ED25519 = 'ED25519'
    RSA = 'RSA'


DEFAULT_KEY_HASH_ALGORITHM = KeyHashAlgorithm.SHA_256

SSH_AUTH_SOCK_ENV_VAR = 'SSH_AUTH_SOCK'
SSH_AGENT_NO_KEYS_MESSAGE = 'The agent has no identities.'

AGENT_KEY_IDENTITY_ATTRIBUTES = (
    'comment',
    'hash',
)
SSH_KEY_IDENTITY_ATTRIBUTES = (
    'comment',
    'hash',
    'key_type',
)
