#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for ssh_assets.authorized_keys submodule tests
"""
from ..conftest import MOCK_DATA

VALID_AUTHORIZED_KEYS_FILE = MOCK_DATA.joinpath('authorized_keys/valid.txt')
EXPECTED_KEYS_COUNT = 8

INVALID_ENTRY = 'AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4/WBdHPxuALr1iYzUT21 info@example.net'
INVALID_BASE64_ENTRY = 'pty ssh-ed25519 info@example.net'
INVALID_FORMAT_ENTRY = 'AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4 ssh-rsa'

VALID_ENTRY = 'pty ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJwd1cg2Uusi9BXiNP041Mav4/WBdHPxuALr1iYzUT21 info@example.net'
