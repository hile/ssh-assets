#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Exceptions raised by SSH key processing
"""


class SSHAssetsError(Exception):
    """
    Generic errors raised by SSH assets tool
    """


class SSHKeyError(Exception):
    """
    Error raised by SSH key processing
    """
