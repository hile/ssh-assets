"""
Constants for OpenSSH authorized keys parsing
"""

DEFAULT_AUTHORIZED_KEYS_FILE = '~/.ssh/authorized_keys'

# Valid key types in authorized_keys files
KEY_TYPES = (
    'ecdsa-sha2-nistp256',
    'ecdsa-sha2-nistp384',
    'ecdsa-sha2-nistp521',
    'sk-ecdsa-sha2-nistp256@openssh.com',
    'sk-ssh-ed25519@openssh.com',
    'ssh-dss',
    'ssh-ed25519',
    'ssh-rsa',
)

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
