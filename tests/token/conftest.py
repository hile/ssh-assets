#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Pytest fixtures for the ssh_agents.token unit tests
"""
import pytest

from ssh_assets.token.client import CLIENT_CONFIG_TOKEN_STRING_CLASSES
from ssh_assets.token.server import SERVER_CONFIG_TOKEN_STRING_CLASSES

DUMMY_VALUE = 'dummy-string'


@pytest.fixture(params=CLIENT_CONFIG_TOKEN_STRING_CLASSES)
def client_token_loader(request):
    """
    Fixture to return all client token parser classes from CLIENT_CONFIG_TOKEN_STRING_CLASSES
    """
    yield request.param


@pytest.fixture(params=SERVER_CONFIG_TOKEN_STRING_CLASSES)
def server_token_loader(request):
    """
    Fixture to return all server token parser classes from SERVER_CONFIG_TOKEN_STRING_CLASSES
    """
    yield request.param
