"""
Unit tests for ssh_assets.keys.filter_set module
"""
from ssh_assets.keys.filter_set import SshKeyFilterSet


def test_filter_set_properties(mock_session):
    """
    Test basic properties of fite
    """
    assert isinstance(mock_session.key_filter_set, SshKeyFilterSet)
    # Each filter set property access returns unique filter set
    assert mock_session.key_filter_set.__hash__ != mock_session.key_filter_set.__hash__
