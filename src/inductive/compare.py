"""
# compare

Comparing values, comparable values.
"""

from __future__ import annotations

import collections.abc
import enum
import typing


class Compare(enum.Enum):
    """
    A simple type that represents the result of an ordering
    comparison between a left value and a right value.

    >>> some_comparing_function(left, right)
    Compare.LESS  # left < right
    >>> some_comparing_function(left, right)
    Compare.EQUAL  # left == right
    >>> some_comparing_function(left, right)
    Compare.GREATER  # left > right
    """

    LESS = -1
    """left < right"""

    EQUAL = 0
    """left == right"""

    GREATER = 1
    """left > right"""


class Comparable[Other](typing.Protocol):
    """
    A type T is `Comparable` with a type U if it implements the
    method `compare` with respect to U.
    """

    def compare(self, other: Other, /) -> Compare:
        """
        Compare `self` with `other`.
        """
        ...


type SelfComparable = Comparable[SelfComparable]
"""
`SelfComparable` is a specialization of the `Comparable`
protocol where the right handside has the same type as the left
one.
"""

type Comparator[T, U] = collections.abc.Callable[[T, U], Compare]

LESS = Compare.LESS
EQUAL = Compare.EQUAL
GREATER = Compare.GREATER
