"""
# list

WARNING: It is advised NOT to use this module for computing large
datasets. Also, raising the maximum recursion limit is recommended.

Inductive definition of singly-linked lists.

"""
# ruff: noqa: PLR0904

from __future__ import annotations

import abc
import collections.abc
import typing

import attrs
import option

from inductive import compare
from inductive import nat


@attrs.frozen
class _ListInterface[T](abc.ABC, collections.abc.Sequence[T]):
    """
    Abstract class to enforce the list interface on both `Nil` and
    `Cons`.
    """

    @abc.abstractmethod
    def length(self) -> nat.Nat:
        """
        Return the length of the list.

        >>> L[()].length()
        0
        >>> L[3, 5, 2].length()
        3
        """

    # *- Methods -* #

    # Predicates

    @abc.abstractmethod
    def for_all(self, predicate: collections.abc.Callable[[T], bool]) -> bool:
        """
        Find whether `predicate(item)` is `True` for all items
        of the list.
        """

        return self.map(predicate).fold(
            lambda left, right: left and right,
            initial_value=True,
        )

    @abc.abstractmethod
    def for_any(self, predicate: collections.abc.Callable[[T], bool]) -> bool:
        """
        Find whether `predicate(item)` is `True` for at least
        one item in the list.
        """

        return self.map(predicate).fold(
            lambda left, right: left or right,
            initial_value=False,
        )

    @abc.abstractmethod
    def for_only_one(
        self,
        predicate: collections.abc.Callable[[T], bool],
    ) -> bool:
        """
        Find whether `predicate(item)` is `True` for one and
        only one item in the list.
        """

        return self.keep(predicate).length() == nat.one

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """
        Return `True` if the list is empty.

        >>> L[()].is_empty()
        True
        >>> L[3, 5, 2].is_empty()
        False
        """

    def contains(self, item: T, /) -> bool:
        """
        Return `True` if `item` is in the list.

        >>> L[3, 5, 2].contains(5)
        True
        >>> L[3, 5, 2].contains(7)
        False
        >>> L[()].contains(4)
        False
        """

        return item in self

    @abc.abstractmethod
    def is_unique(self, item: T, /) -> bool:
        """
        Return `True` if `item` appears exactly once in the list.
        """

    # Arrangement

    def arrange(
        self,
        function: collections.abc.Callable[[T], nat.Nat],
    ) -> option.Option[List[T]]:
        """
        Arrange the list by getting the new index of each item
        using `function`.

        Returns `Nothing` if `function` produces either the same
        index for two different items or an index that is out of
        bounds.
        """

        return self.arrange_with_index(lambda _, item: function(item))

    def arrange_unsafe(
        self,
        function: collections.abc.Callable[[T], nat.Nat],
    ) -> List[T]:
        """
        Same as `arrange`. Only use if you are certain that
        `function` produces unique indexes for each item and
        that are within the list bounds.
        """

        return self.arrange_with_index_unsafe(lambda _, item: function(item))

    @abc.abstractmethod
    def arrange_with_index(
        self,
        function: collections.abc.Callable[[nat.Nat, T], nat.Nat],
    ) -> option.Option[List[T]]:
        """
        Same as `arrange`, but `function` also takes the current
        index of the item as an argument.

        Like its non-indexed counterpart, it returns `Nothing`
        if `function` produces either the same index for two
        different items or an index that is out of bounds.
        """

    def arrange_with_index_unsafe(
        self,
        function: collections.abc.Callable[[nat.Nat, T], nat.Nat],
    ) -> List[T]:
        """
        Same as `arrange_with_index`. Only use if you are
        certain that `function` produces unique indexes for each
        item and that are within the list bounds.
        """  # noqa: DOC501

        match self.arrange_with_index(function):
            case option.Nothing():
                message = "invariant violation: function is not injective"
                raise AssertionError(message)
            case option.Some(list):
                return list

    @abc.abstractmethod
    def make_first(self, index: nat.Nat) -> option.Option[List[T]]:
        """
        `L[item0, ..., itemI, ..., itemN].make_first(I)`
        produces `Some([itemI, item0, ..., itemN])`.

        Returns `Nothing` if `index` is out of bounds or the
        list is empty.
        """

        if not (nat.zero <= index < self.length()):
            return option.Nothing()

        def function(i: nat.Nat, _: T) -> nat.Nat:
            # We found our element, move it to the beginning
            if i == index:
                return nat.zero

            # Otherwise, we shift it to the right to leave some
            # space for the new first element
            return nat.succ(i)

        return self.arrange_with_index(function)

    def reverse(self) -> List[T]:
        """
        Return a reversed version of the list.
        """

        last_index = self.length() - nat.one

        return self.arrange_with_index_unsafe(
            lambda index, _: last_index - index,
        )

    @abc.abstractmethod
    def sort(self, comparator: compare.Comparator[T, T]) -> List[T]:
        """
        Return a sorted version of the list, where items are
        ordered using the provided `comparator` function.
        """

    def sort_by(
        self,
        *,
        key: collections.abc.Callable[[T], compare.Comparable[T]],
    ) -> List[T]:
        """
        Return a sorted version of the list, where items are
        ordered by mapping them to a type where comparison is
        supported using the `key` function.
        """

        return self.sort(lambda left, right: key(left).compare(right))

    def sort_comparable[ComparableT: compare.SelfComparable](
        self: List[ComparableT],  # pyright: ignore[reportGeneralTypeIssues]
    ) -> List[ComparableT]:
        """
        Return a sorted version of the list where its items must
        be comparable.
        """

        return self.sort_by(key=lambda x: x)

    # Adding, removing

    def prepend(self, item: T) -> Cons[T]:
        """
        `list.prepend(item)` produces a new list [item, ...list].
        """

        return Cons(item, typing.cast("List[T]", self))

    @abc.abstractmethod
    def append(self, last: T) -> Cons[T]:
        """
        `list.append(item)` produces a new list [...list, item].
        """

    @abc.abstractmethod
    def concatenate(self, other: List[T]) -> List[T]:
        """
        `list.concatenate(other)` produces a new list
        [...list, ...other].
        """

    # Remove should essentially be `make_first() >> as_tuple()`
    @abc.abstractmethod
    def remove(self, index: nat.Nat) -> option.Option[tuple[T, List[T]]]:
        """
        `L[item0, ..., itemI, ..., itemN].remove(I)` produces
        `(itemI, [item0, ..., itemN])`.
        """

    # Counting, searching

    @abc.abstractmethod
    def occurrences(self, item: T) -> nat.Nat:
        """
        Count the number of times `item` appears in the list.
        """

    def find(
        self,
        predicate: collections.abc.Callable[[T], bool],
    ) -> option.Option[T]:
        """
        Return the first item of the list for which
        `predicate(item)` is `True`.
        """

        return self.find_with_index(lambda _, item: predicate(item))

    @abc.abstractmethod
    def find_with_index(
        self,
        predicate: collections.abc.Callable[[nat.Nat, T], bool],
        /,
    ) -> option.Option[T]:
        """
        Same as `find`, but `predicate` also takes the item's
        index as argument.
        """

    # Computing, filtering

    @abc.abstractmethod
    def map[U](self, function: collections.abc.Callable[[T], U]) -> List[U]:
        """
        `L[item0, ..., itemN].map(function)` produces a new list
        `[function(item0), ..., function(itemN)]`.
        """

    @abc.abstractmethod
    def flatmap[U](
        self,
        function: collections.abc.Callable[[T], List[U]],
    ) -> List[U]:
        """
        `L[item0, ..., itemN].map(function)` produces a new list
        `[...function(item0), ..., ...function(itemN)]`.
        """

    @abc.abstractmethod
    def combine[U, V](
        self,
        other: List[U],
        function: collections.abc.Callable[[T, U], V],
    ) -> List[V]:
        """
        `L[a0, ..., aN].combine(L[b0, ..., bN], function)`
        produces `L[function(a0, b0), ..., function(aN, bN)]`
        """

    @abc.abstractmethod
    def keep(
        self,
        predicate: collections.abc.Callable[[T], bool],
    ) -> List[T]:
        """
        Keep the items for which `predicate(item)` is `True`.

        Inverse of `discard`.
        """

    def discard(
        self,
        predicate: collections.abc.Callable[[T], bool],
    ) -> List[T]:
        """
        Discard the items for which `predicate(item)` is `True`.

        Inverse of `keep`.
        """

        return self.keep(lambda item: not predicate(item))

    @abc.abstractmethod
    def fold[U](
        self,
        function: collections.abc.Callable[[U, T], U],
        initial_value: U,
    ) -> U:
        """
        `L[item0, ..., itemN].fold(OP, init)` is equivalent to
        `init OP item0 OP ... OP itemN`.
        """

    @abc.abstractmethod
    def fold_cons(
        self,
        function: collections.abc.Callable[[T, T], T],
    ) -> option.Option[T]:
        """
        `L[item0, item1, ..., itemN].fold_cons(OP)` produces
        `item0 OP item1 OP ... OP itemN`.

        Returns `Nothing` if the list is empty.
        """

    @abc.abstractmethod
    def accumulate(
        self,
        function: collections.abc.Callable[[T, T], T],
        initial_value: T,
    ) -> List[T]:
        """
        Similar to `fold`, but keeps the intermediate values.
        """

    @abc.abstractmethod
    def accumulate_cons(
        self,
        function: collections.abc.Callable[[T, T], T],
    ) -> option.Option[List[T]]:
        """
        Similar to `fold_cons`, but keeps the intermediate
        values.
        """

    @abc.abstractmethod
    def deduplicate(self) -> List[T]:
        """
        Make every item of the list unique by removing
        additional appearences of them.
        """

    @abc.abstractmethod
    def without_first(self) -> List[T]:
        """
        `L[item0, item1, ..., itemN].without_first()` produces
        `L[item1, ..., itemN]`.

        Returns the original list if it is empty.
        """

    @abc.abstractmethod
    def without_last(self) -> List[T]:
        """
        `L[item0, ..., itemN-1, itemN].without_last()` produces
        `L[item0, ..., itemN-1]`.

        Returns the original list if it is empty.
        """

    # *- Portions -* #

    def cut(
        self,
        predicate: collections.abc.Callable[[T], bool],
    ) -> tuple[List[T], List[T]]:
        """
        Cut the list in two parts before the item for which
        `predicate(item)` is `True`.
        """

        return self.cut_with_index(lambda _, item: predicate(item))

    @abc.abstractmethod
    def cut_with_index(
        self,
        predicate: collections.abc.Callable[[nat.Nat, T], bool],
    ) -> tuple[List[T], List[T]]:
        """
        Same as `cut` with `predicate` also taking the index of
        the item as argument.
        """

    def cut_at(self, index: nat.Nat) -> option.Option[tuple[List[T], List[T]]]:
        """
        Cut the list before the `index` into a pair of two lists.

        Returns `Nothing` if `index` is out of bounds.
        For a more lax version, check out `cut_at_clamped`.
        """

        pass

    def cut_at_clamped(self, index: nat.Nat) -> tuple[List[T], List[T]]:
        pass

    # *- Iteration utils -* #

    @abc.abstractmethod
    def pairwise(self) -> List[tuple[T, T]]:
        """
        `L[item0, item1, item2, ..., itemN].pairwise()` produces
        `[(item0, item1), (item1, item2), ..., (itemN-1, itemN)]`.
        """


@attrs.frozen
@typing.final
class Nil(_ListInterface[typing.Any]):
    """
    `Nil` represents the empty list.
    """

    # *- Sequence protocol -* #

    @typing.override
    def __getitem__(self, index: int | slice) -> typing.Any:
        message = "list index out of range"
        raise IndexError(message)

    @typing.override
    def __len__(self) -> int:
        return 0

    # *- Methods -* #

    @typing.override
    def length(self) -> nat.Zero:
        return nat.Zero()

    # *- Operators -* #


@attrs.frozen
@typing.final
class Cons[T](_ListInterface[T]):
    """
    `Cons` represents a value paired with the rest of the list.
    """

    value: T
    next: List[T]

    def as_tuple(self) -> tuple[T, List[T]]:
        """
        `Cons(value, next).as_tuple()` produces the tuple
        `(value, next)`.
        """

        match self:
            case Cons(value, next):
                return value, next

    def fold_cons_safe(
        self,
        function: collections.abc.Callable[[T, T], T],
    ) -> T:
        """
        Same as `fold_cons`, but returns the value directly
        instead of an `Option`. For this reason, it is only
        available on lists that are guaranteed to be `Cons`.
        """

        match self:
            case Cons(value, next):
                return next.fold(function, value)


type List[T] = Nil | Cons[T]

# *- Specialized methods -* #
# Specialized methods are functions on lists where the items
# have a specific type.


def join[T](lst: List[List[T]]) -> List[T]:
    """
    Concatenate all the lists in list into one.

    >>> join(L[L[3, 5, 2], L[7, 1, 9], L[4, 8, 6]])
    [3, 5, 2, 7, 1, 9, 4, 8, 6]
    >>> join(L[()])
    []
    """

    return lst.flatmap(lambda x: x)


def map_apply[T, U](
    lst: List[collections.abc.Callable[[T], U]],
    argument: T,
) -> List[U]:
    """
    Apply each function of the list to `argument` and return a
    list of the results.
    """

    return lst.map(lambda function: function(argument))


def map_apply_binary[T, U, V](
    lst: List[collections.abc.Callable[[T, U], V]],
    left: T,
    right: U,
) -> List[V]:
    """
    Apply each binary function of the list to `left` and `right`
    and return a list of the results.
    """

    return lst.map(lambda function: function(left, right))


def transpose[T](lst: List[List[T]]) -> List[List[T]]:
    """
    Swap the rows and the columns of the list.

    >>> transpose(L[L[3, 5, 2], L[7, 1, 9], L[4, 8, 6]])
    [[3, 7, 4], [5, 1, 8], [2, 9, 6]]
    >>> transpose(L[()])
    []
    >>> transpose(transpose(my_matrix)) == my_matrix
    True
    """
