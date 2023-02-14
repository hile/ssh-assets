"""
Unit tests for ssh_assets.keys.base module
"""

import pytest

from ssh_assets.exceptions import SSHKeyError
from ssh_assets.keys.constants import KeyHashAlgorithm
from ssh_assets.keys.base import SSHKeyLoader

MOCK_BITS = 2048
UNEXPECTED_ATTRIBUTE = 'nosuchthing'
UNEXPECTED_KEY_LINES = (
    '1234 SHA256:AABBCC',
    '',
)
MOCK_FIRST_KEY_ATTRIBUTES = {
    'bits': MOCK_BITS,
    'hash': 'AABBCC',
    'comment': '',
    'key_type': 'RSA'
}
MOCK_SECOND_KEY_ATTRIBUTES = {
    'bits': MOCK_BITS,
    'hash': 'CACCAC',
    'comment': 'Test key',
    'key_type': 'RSA'
}


# pylint: disable=too-few-public-methods
class MockInvalidKeyClass:
    """
    Mock an invalid key class with missing compare operation fields
    """
    bits = MOCK_BITS
    comment = 'This mock class is missing required compare fields'


def test_ssh_key_loader_attributes():
    """
    Test attributes of SSH key loader base class
    """
    loader = SSHKeyLoader()
    assert loader.__key_attributes__ == {}


def test_ssh_key_loader_invalid_hash_algorithm():
    """
    Test initializing SSHKeyLoader with various unsupported values for hash_algorithm
    value: note that passing valid text Enum value is also not supported
    """
    for testcase in (None, '', KeyHashAlgorithm.SHA_256.value):
        with pytest.raises(SSHKeyError):
            SSHKeyLoader(testcase)


def test_ssh_key_loader_invalid_attribute():
    """
    Test getting attributes of SSH key loader base class, both a valid attribute and
    unexpected attribute
    """
    loader = SSHKeyLoader()
    loader.__key_attributes__ = {
        'bits': MOCK_BITS
    }
    assert loader.bits == MOCK_BITS
    with pytest.raises(SSHKeyError):
        loader.__get_key_attribute__(UNEXPECTED_ATTRIBUTE)


def test_ssh_key_loader_invalid_input_line():
    """
    Test exception raised when loading unexpected lines as parser output
    """
    loader = SSHKeyLoader()
    for testcase in UNEXPECTED_KEY_LINES:
        with pytest.raises(SSHKeyError):
            loader.__parse_key_info_line__(testcase)


def test_ssh_key_loader_load_exception():
    """
    Ensure base class triggers NotImplementedError for base class methods
    """
    with pytest.raises(NotImplementedError):
        SSHKeyLoader().__load_key_attributes__()


def test_ssh_key_loader_compare(tmp_path):
    """
    Test comparing of base classes for SSH keys
    """
    a = SSHKeyLoader(hash_algorithm=KeyHashAlgorithm.SHA_256)
    b = SSHKeyLoader(hash_algorithm=KeyHashAlgorithm.SHA_256)
    invalid = MockInvalidKeyClass()

    with pytest.raises(NotImplementedError):
        assert a == b

    a.__key_attributes__ = MOCK_FIRST_KEY_ATTRIBUTES
    b.__key_attributes__ = MOCK_SECOND_KEY_ATTRIBUTES

    assert a == a  # pylint: disable=comparison-with-itself
    assert a <= a  # pylint: disable=comparison-with-itself

    assert a == a.hash  # pylint: disable=comparison-with-itself
    assert a < b.hash

    assert not a == b  # pylint: disable=unneeded-not
    assert a != b

    assert a < b
    assert a <= b
    assert b > a
    assert b >= a

    a.path = tmp_path
    b.path = tmp_path.joinpath('b-key')
    assert a == tmp_path
    assert a < b.path

    with pytest.raises(TypeError):
        assert a == invalid
    with pytest.raises(TypeError):
        assert a < invalid
