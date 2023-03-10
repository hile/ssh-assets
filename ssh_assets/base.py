#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base classes
"""
from operator import ge, gt, le, lt
from typing import Any, Callable


class RichComparisonObject:
    """
    Common base class for implementing a rich comparison object
    """
    __compare_attributes__ = ()

    def __compare__(self, operator: Callable, default: bool, other: Any) -> bool:
        """
        Common compare method for sorting
        """
        if isinstance(other, str):
            return operator(str(self), other)
        for attr in self.__compare_attributes__:
            a = getattr(self, attr)
            if not hasattr(other, attr):
                raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
            b = getattr(other, attr)
            if a != b:
                return operator(a, b)
        return default

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return str(self) == other
        for attr in self.__compare_attributes__:
            a = getattr(self, attr)
            if not hasattr(other, attr):
                raise TypeError(f'Comparing {type(self)} to {type(other)} is not supported')
            b = getattr(other, attr)
            if a != b:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        return self.__compare__(lt, False, other)

    def __gt__(self, other: Any) -> bool:
        return self.__compare__(gt, False, other)

    def __le__(self, other: Any) -> bool:
        return self.__compare__(le, True, other)

    def __ge__(self, other: Any) -> bool:
        return self.__compare__(ge, True, other)
