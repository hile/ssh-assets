#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for OpenSSH authorized keys parsing
"""
from enum import Enum

DEFAULT_AUTHORIZED_KEYS_FILE = '~/.ssh/authorized_keys'


class SshAuthorizedKeysKeyType(Enum):
    """'
    Valid SSH key types in authorized keys lines
    """
    ECDSA_NISTP_256 = 'ecdsa-sha2-nistp256'
    ECDSA_NISTP_384 = 'ecdsa-sha2-nistp384'
    ECDSA_NISTP_512 = 'ecdsa-sha2-nistp512'
    SK_ECDSA_SHA2_NISTP_256 = 'sk-ecdsa-sha2-nistp256@openssh.com'
    SK_ED25519 = 'sk-ssh-ed25519@openssh.com'
    DSS = 'ssh-dss'
    ED25519 = 'ssh-ed25519'
    RSA = 'ssh-rsa'


# Authorized keys options with no value
AUTHRORIZED_KEYS_OPTION_FLAGS = (
    'agent-forwarding',
    'cert-authority',
    'no-agent-forwarding',
    'no-port-forwarding',
    'no-pty',
    'no-user-rc',
    'no-X11-forwarding',
    'port-forwarding',
    'pty',
    'no-touch-required',
    'verify-required',
    'restrict',
    'user-rc',
    'X11-forwarding',
)

# Authorized keys options that require a value for the option
AUTHRORIZED_KEYS_OPTION_VALUE_FLAGS = (
    'command',
    'environment',
    'expiry-time',
    'from',
    'permitlisten',
    'permitopen',
    'principals',
    'tunnel',
)
