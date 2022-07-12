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


DEFAULT_KEY_HASH_ALGORITHM = KeyHashAlgorithm.SHA_256

SSH_AUTH_SOCK_ENV_VAR = 'SSH_AUTH_SOCK'
SSH_AGENT_NO_KEYS_MESSAGE = 'The agent has no identities.'
