"""
Common base classes
"""

from operator import ge, gt, le, lt


class RichComparisonObject:
    """
    Common base class for implementing a rich comparison object
    """
    __compare_attributes__ = ()

    def __compare__(self, operator, default, other):
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

    def __eq__(self, other):
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

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.__compare__(lt, False, other)

    def __gt__(self, other):
        return self.__compare__(gt, False, other)

    def __le__(self, other):
        return self.__compare__(le, True, other)

    def __ge__(self, other):
        return self.__compare__(ge, True, other)
