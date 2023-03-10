#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common token parsing base classes for SSH client and server configuration tokens
"""
import re

# All allowed letter tags in client and server tokens
# Note: client and server token may have different meaning for same letter
RE_TOKEN = re.compile(r'%[CDFHIKLTUdfhiklnprstu%]')


# pylint: disable=too-few-public-methods
class TokenStringValidator:
    """
    Validator for configuration strings with tokens
    """
    __option__ = ''
    __suppported_tokens__ = ()

    @property
    def expected_tokens(self):
        """
        Return list of expected tokens for this validator
        """
        return [token.value for token in self.__suppported_tokens__]

    def validate(self, value):
        """
        Validate the token string

        This method detects any token variables and ensures the variables used in the string are
        supported by the current token option child class

        Raises NotImplementedError for base class (__supported_tokens__ is empty)
        """
        if not self.__suppported_tokens__:
            raise NotImplementedError('SSH token parser must define tokens in __supported_tokens__')

        tokens = []
        scanner = RE_TOKEN.scanner(value)
        result = scanner.search()
        while result:
            token = result.string[result.start():result.end()]
            if token not in self.expected_tokens:
                raise ValueError(f'Unexpected {self.__option__} token: {token} in string "{value}"')
            tokens.append(token)
            result = scanner.search()
        return tokens
