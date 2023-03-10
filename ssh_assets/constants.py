#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for ssh_assets python module
"""
from pathlib import Path

USER_CONFIGURATION_FILE = Path('~/.ssh/assets.yml').expanduser()

NO_KEYS_CONFIGURED = 'No keys are configured in the SSH assets configuration file'
NO_KEYS_MATCH = 'No keys matching query arguments detected'
