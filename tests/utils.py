"""
Unit test utility methods for ssh_assets.keys module
"""

from ssh_assets.keys.base import (
    KEY_COMPARE_ATTRIBUTES,
    KEY_INTEGER_ATTRIBUTES,
    KEY_STRING_ATTRIBUTES,
)


def validate_key(key, key_class):
    """
    Validate some basic attributes of SSH key from agent
    """
    assert isinstance(key, key_class)
    assert isinstance(key.__repr__(), str)

    for attr in KEY_COMPARE_ATTRIBUTES:
        assert hasattr(key, attr)
        assert getattr(key, attr) is not None

    for attr in KEY_INTEGER_ATTRIBUTES:
        assert hasattr(key, attr)
        assert isinstance(getattr(key, attr), int)

    # Note: string fields MAY be empty strings
    for attr in KEY_STRING_ATTRIBUTES:
        assert hasattr(key, attr)
        assert isinstance(getattr(key, attr), str)

    # This must not cause any errors, it's a dummy method
    key.__load_key_attributes__()
