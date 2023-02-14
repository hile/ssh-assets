"""
Unit tests for ssh_assets.keys.filter_set module
"""
from ssh_assets.configuration.keys import SshKeyConfiguration
from ssh_assets.keys.filter_set import (
    SshKeyFilterSet,
    filter_key_available,
    filter_key_groups,
    filter_key_loaded,
    filter_key_names,
)

from ..conftest import (
    MOCK_BASIC_CONFIG_EXISTING_GROUP,
    MOCK_BASIC_CONFIG_EXISTING_GROUP_KEY_COUNT,
    MOCK_BASIC_CONFIG_EXISTING_KEY,
    MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT,
    MOCK_BASIC_CONFIG_KEYS_COUNT,
    MOCK_UNKNOWN_GROUP_NAME,
    MOCK_UNKNOWN_KEY_NAME,
)


def validate_key_list(matches) -> None:
    """
    Ensure returned value is list of SshKeyConfiguration objects
    """
    assert isinstance(matches, list)
    for item in matches:
        assert isinstance(item, SshKeyConfiguration)


def test_filter_set_properties(mock_session):
    """
    Test basic properties of fite
    """
    assert isinstance(mock_session.key_filter_set, SshKeyFilterSet)
    # Each filter set property access returns unique filter set
    assert mock_session.key_filter_set.__hash__ != mock_session.key_filter_set.__hash__


def test_filter_set_filter_key_available_true(mock_session):
    """
    Test the filter_key_available function directly with 'true' as available flag value
    """
    default = filter_key_available(mock_session.configuration.keys)
    matches = filter_key_available(mock_session.configuration.keys, True)
    assert default == matches
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


def test_filter_set_filter_key_available_false(mock_session):
    """
    Test the filter_key_available function directly with 'true' as available flag value
    """
    default = filter_key_available(mock_session.configuration.keys)
    matches = filter_key_available(mock_session.configuration.keys, False)
    assert default != matches
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_KEYS_COUNT - MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


def test_filter_set_filter_key_loaded_true(mock_session):
    """
    Test the filter_key_loaded function directly with 'true' as loaded flag value
    """
    default = filter_key_loaded(mock_session.configuration.keys)
    matches = filter_key_loaded(mock_session.configuration.keys, True)
    assert default == matches
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


def test_filter_set_filter_key_loaded_false(mock_session):
    """
    Test the filter_key_available function directly with 'true' as loaded flag value
    """
    default = filter_key_loaded(mock_session.configuration.keys)
    matches = filter_key_loaded(mock_session.configuration.keys, False)
    assert default != matches
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_KEYS_COUNT - MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


def test_filter_set_filter_key_groups_no_groups(mock_session):
    """
    Test the filter_key_groups function directly without groups to filter, returning all keys
    """
    matches = filter_key_groups(mock_session, mock_session.configuration.keys, [])
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_KEYS_COUNT


def test_filter_set_filter_key_groups_no_match(mock_session):
    """
    Test the filter_key_groups function directly with unexpected group names
    """
    matches = filter_key_groups(mock_session, mock_session.configuration.keys, [MOCK_UNKNOWN_GROUP_NAME])
    validate_key_list(matches)
    assert matches == []


def test_filter_set_filter_key_groups_match_single_group(mock_session):
    """
    Test the filter_key_groups function directly with known group name
    """
    matches = filter_key_groups(mock_session, mock_session.configuration.keys, [MOCK_BASIC_CONFIG_EXISTING_GROUP])
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_EXISTING_GROUP_KEY_COUNT


def test_filter_set_filter_key_groups_match_mixed_groups(mock_session):
    """
    Test the filter_key_groups function directly with known group name and
    with the unknonw group name mixed
    """
    matches = filter_key_groups(
        mock_session,
        mock_session.configuration.keys,
        [MOCK_BASIC_CONFIG_EXISTING_GROUP, MOCK_UNKNOWN_GROUP_NAME]
    )
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_EXISTING_GROUP_KEY_COUNT


def test_filter_set_filter_key_names_no_names(mock_session):
    """
    Test the filter_key_names function directly with no key names to filter, returning all keys
    """
    matches = filter_key_names(mock_session.configuration.keys, [])
    validate_key_list(matches)
    assert len(matches) == MOCK_BASIC_CONFIG_KEYS_COUNT


def test_filter_set_filter_key_names_no_match(mock_session):
    """
    Test the filter_key_names function directly with unexpected key names
    """
    matches = filter_key_names(mock_session.configuration.keys, [MOCK_UNKNOWN_KEY_NAME])
    validate_key_list(matches)
    assert matches == []


def test_filter_set_filter_key_names_match(mock_session):
    """
    Test the filter_key_names function directly with known key name
    """
    matches = filter_key_names(mock_session.configuration.keys, [MOCK_BASIC_CONFIG_EXISTING_KEY])
    validate_key_list(matches)
    assert len(matches) == 1


def test_filter_set_filter_key_names_match_mixed(mock_session):
    """
    Test the filter_key_names function directly with known key name and invalid key name
    """
    matches = filter_key_names(
        mock_session.configuration.keys,
        [
            MOCK_BASIC_CONFIG_EXISTING_KEY,
            MOCK_UNKNOWN_KEY_NAME,
        ]
    )
    validate_key_list(matches)
    assert len(matches) == 1


def test_filter_set_class_filter_groups(mock_session):
    """
    Test calling filter_groups method of SshKeyFilterSet, returning a filter set of filtered keys
    """
    matches = mock_session.key_filter_set.filter_groups([MOCK_BASIC_CONFIG_EXISTING_GROUP])
    assert isinstance(matches, SshKeyFilterSet)
    assert len(matches.keys) == MOCK_BASIC_CONFIG_EXISTING_GROUP_KEY_COUNT


def test_filter_set_class_filter_names(mock_session):
    """
    Test calling filter_names method of SshKeyFilterSet, returning a filter set of filtered keys
    """
    matches = mock_session.key_filter_set.filter_names([MOCK_BASIC_CONFIG_EXISTING_KEY])
    assert isinstance(matches, SshKeyFilterSet)
    assert len(matches.keys) == 1


def test_filter_set_class_filter_available(mock_session):
    """
    Test calling filter_available method of SshKeyFilterSet, returning a filter set of filtered keys
    """
    default = mock_session.key_filter_set.filter_available()
    matches = mock_session.key_filter_set.filter_available(True)
    assert default.keys == matches.keys
    assert len(matches.keys) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT


def test_filter_set_class_filter_loaded(mock_session):
    """
    Test calling filter_loaded method of SshKeyFilterSet, returning a filter set of filtered keys
    """
    default = mock_session.key_filter_set.filter_loaded()
    matches = mock_session.key_filter_set.filter_loaded(True)
    assert default.keys == matches.keys
    assert len(matches.keys) == MOCK_BASIC_CONFIG_AVAILABLE_KEYS_COUNT
