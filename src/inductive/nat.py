"""
# nat

WARNING: It is advised NOT to use this module for computing large numbers.
Also, raising the maximum recursion limit is recommended.

Inductive definition of natural numbers, following Peano axioms.

Basic arithmetic operators are defined using the built-in
operators, with the following nuance: `/` is considered as the
"strict" division (returns an `Option`) whereas `//` is similar
to Rocq, that is, n // 0 = 0. The modulo operator (`%`) is based
on the latter.
"""
# ruff: noqa: PLR0904

from __future__ import annotations

import typing

import attrs
import option

if typing.TYPE_CHECKING:  # pragma: no cover
    import collections.abc


@attrs.frozen
@typing.final
class Zero:
    """
    `Zero` represents the number 0.
    """

    # *- Comparison -* #
    # equality is handled by attrs

    def __gt__(self, other: Nat, /) -> typing.Literal[False]:
        return False

    def __ge__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return False

    def __lt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return True

    def __le__(self, other: Nat, /) -> typing.Literal[True]:
        return True

    # *- Arithmetic -* #

    def __add__[N: Nat](self, other: N, /) -> N:
        return other

    def __radd__[N: Nat](self, other: N, /) -> N:  # pragma: no cover
        return other

    def __sub__(self, other: Nat, /) -> Zero:
        return self

    def __rsub__[N: Nat](self, other: N, /) -> N:  # pragma: no cover
        return other

    def __mul__(self, other: Nat, /) -> Zero:
        return self

    def __rmul__(self, other: Nat, /) -> Zero:  # pragma: no cover
        return self

    # We implement divmod for completeness
    def __divmod__(self, other: Nat, /) -> option.Option[tuple[Zero, Zero]]:
        match other:
            case Zero():
                return option.Nothing()
            case Succ():
                return option.Some((Zero(), Zero()))

    def __truediv__(self, other: Nat, /) -> option.Option[Zero]:
        match other:
            case Zero():
                return option.Nothing()
            case Succ():
                return option.Some(self)

    def __rtruediv__(self, other: Nat, /) -> option.Nothing:  # pragma: no cover
        return option.Nothing()

    def __floordiv__(self, other: Nat, /) -> Zero:
        return self

    def __rfloordiv__(self, other: Nat, /) -> Zero:  # pragma: no cover
        return self

    def __mod__(self, other: Nat, /) -> Zero:
        return self

    def __rmod__(self, other: Nat, /) -> Zero:  # pragma: no cover
        return self

    # *- Type conversion -* #

    def __abs__(self) -> typing.Self:
        return self

    def __bool__(self) -> typing.Literal[False]:
        return False

    def __complex__(self) -> complex:
        return 0j

    def __float__(self) -> float:
        return 0.0

    def __int__(self) -> int:
        return 0

    def __str__(self) -> str:
        return "0"

    def __repr__(self) -> str:
        return "Zero"

    def __bytes__(self) -> bytes:
        return b""

    # *- Methods -* #

    def double(self) -> Zero:
        """
        Return the double of the number.
        """

        return self

    def square(self) -> Zero:
        """
        Return the number multiplied by itself.
        """

        return self

    def is_odd(self) -> typing.Literal[False]:  # noqa: PLR6301
        """
        Return whether the number is odd or not.
        """

        return False

    def is_even(self) -> typing.Literal[True]:  # noqa: PLR6301
        """
        Return whether the number is even or not.
        """

        return True

    def as_integer_ratio(  # noqa: PLR6301
        self: Nat,
    ) -> tuple[typing.Literal[0], typing.Literal[1]]:
        """
        Return a pair of integers, whose ratio is equal to the original int.

        The ratio is in lowest terms and has a positive denominator.
        """

        return (0, 1)


@attrs.frozen
@typing.final
class Succ[N: Nat]:
    """
    `Succ[N]` represents the next number after `N`.
    """

    predecessor: N

    # *- Comparison -* #
    # equality is handled by attrs

    def __gt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return self.predecessor > other.predecessor

    def __ge__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return self.predecessor >= other.predecessor

    def __lt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return self.predecessor < other.predecessor

    def __le__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return self.predecessor <= other.predecessor

    # *- Arithmetic -* #

    @typing.overload
    def __add__(self, other: Zero, /) -> typing.Self: ...
    @typing.overload
    def __add__(self, other: Succ[Nat], /) -> Nat: ...

    def __add__(self, other: Nat, /) -> typing.Self | Nat:
        match other:
            case Zero():
                return self
            case Succ():
                # XXX: Pyright fails to infer the type of that
                return Succ(self) + other.predecessor  # pyright: ignore[reportArgumentType, reportUnknownVariableType]

    @typing.overload
    def __sub__(self, other: Zero, /) -> typing.Self: ...
    @typing.overload
    def __sub__(self, other: typing.Self, /) -> Zero: ...
    @typing.overload
    def __sub__(self, other: Succ[Nat], /) -> Nat: ...

    def __sub__(self, other: Nat, /) -> typing.Self | Nat:
        match other:
            case Zero():
                return self
            case Succ():
                return self.predecessor - other.predecessor

    @typing.overload
    def __mul__(self, other: Zero, /) -> Zero: ...
    @typing.overload
    def __mul__[N0: Nat](self: N0, other: Succ[Zero], /) -> N0: ...
    @typing.overload
    def __mul__(self, other: Succ[Nat], /) -> Nat: ...

    def __mul__(self, other: Nat, /) -> typing.Self | Nat:
        match other:
            case Zero():
                return Zero()
            case Succ(predecessor):
                return self + (self * predecessor)

    def __divmod__(self, other: Nat, /) -> option.Option[tuple[Nat, Nat]]:
        def aux(n: Nat, m: Succ[Nat], quotient: Nat) -> tuple[Nat, Nat]:
            if n < m:
                return (quotient, n)
            return aux(n - m, m, Succ(quotient))

        match other:
            case Zero():
                return option.Nothing()
            case Succ():
                # XXX: Pyright incorrectly thinks that self is not a Nat
                return option.Some(aux(self, other, Zero()))  # pyright: ignore[reportArgumentType]

    def __truediv__(self, other: Nat, /) -> option.Option[Nat]:
        match divmod(self, other):
            case option.Nothing():
                return option.Nothing()
            case option.Some((quotient, _)):
                return option.Some(quotient)

    def __floordiv__(self, other: Nat, /) -> Nat:
        match divmod(self, other):
            case option.Nothing():
                return Zero()
            case option.Some((quotient, _)):
                return quotient

    def __mod__(self, other: Nat, /) -> Nat:
        match divmod(self, other):
            case option.Nothing():
                return Zero()
            case option.Some((_, remainder)):
                return remainder

    # *- Type conversion -* #

    def __abs__(self) -> typing.Self:
        return self

    def __bool__(self) -> typing.Literal[True]:
        return True

    def __complex__(self) -> complex:
        return (1.0 + 0.0j) + complex(self.predecessor)  # pyright: ignore[reportArgumentType, reportCallIssue]

    def __float__(self) -> float:
        return 1.0 + float(self.predecessor)  # pyright: ignore[reportArgumentType]

    def __int__(self) -> int:
        return 1 + int(self.predecessor)  # pyright: ignore[reportArgumentType]

    def __str__(self) -> str:  # noqa: PLR0911
        if self == one:
            return "1"
        if self == two:
            return "2"
        if self == three:
            return "3"
        if self == four:
            return "4"
        if self == five:
            return "5"
        if self == six:
            return "6"
        if self == seven:
            return "7"
        if self == eight:
            return "8"
        if self == nine:
            return "9"

        tens, units = self // ten, self % ten

        return str(tens) + str(units)

    def __repr__(self) -> str:
        return f"Succ({self.predecessor!r})"

    def __bytes__(self) -> bytes:
        return b"\x00" + bytes(self.predecessor)  # pyright: ignore[reportArgumentType]

    # *- Methods -* #

    def double(self) -> Nat:
        """
        Return the number added to itself.
        """

        return self + self

    def square(self) -> Nat:
        """
        Return the number multiplied by itself.
        """

        return self * self

    def is_odd(self) -> bool:
        """
        Return whether the number is odd or not.
        """

        # This does NOT end in infinite recursion because
        # `self.predecessor` can be `Zero`
        return not self.predecessor.is_odd()

    def is_even(self) -> bool:
        """
        Return whether the number is even or not.
        """

        # This does NOT end in infinite recursion because
        # `self.predecessor` can be `Zero`
        return not self.predecessor.is_even()

    def as_integer_ratio(self: Nat) -> tuple[int, typing.Literal[1]]:
        """
        Return a pair of integers, whose ratio is equal to the original int.

        The ratio is in lowest terms and has a positive denominator.
        """

        return (int(self), 1)


type Nat = Zero | Succ[Nat]


# *- Digits -* #

zero: typing.Final = Zero()
one: typing.Final = Succ(Zero())
two: typing.Final = Succ(one)
three: typing.Final = Succ(two)
four: typing.Final = Succ(three)
five: typing.Final = Succ(four)
six: typing.Final = Succ(five)
seven: typing.Final = Succ(six)
eight: typing.Final = Succ(seven)
nine: typing.Final = Succ(eight)
ten: typing.Final = Succ(nine)


# *- Methods -* #


def succ[N: Nat](n: N) -> Succ[N]:
    """
    Return the successor of `n`.
    """

    return Succ(n)


@typing.overload
def pred(n: Zero) -> Zero: ...
@typing.overload
def pred[N: Nat](n: Succ[N]) -> N: ...


def pred[N: Nat](n: Zero | Succ[N]) -> Zero | N:
    """
    Return the predecessor of `n` or `Zero`.
    """

    match n:
        case Zero():
            return n
        case Succ(m):
            return m


# *- Constructors from built-in types -* #


@typing.overload
def from_builtin_int(value: typing.Literal[0]) -> option.Some[Zero]: ...
@typing.overload
def from_builtin_int(value: typing.Literal[1]) -> option.Some[Succ[Zero]]: ...
@typing.overload
def from_builtin_int(value: typing.Literal[-1]) -> option.Nothing: ...
@typing.overload
def from_builtin_int(value: int) -> option.Option[Nat]: ...


def from_builtin_int(value: int) -> option.Option[Nat]:
    """
    Construct a `Nat` from a built-in `int`.
    If `value` is negative, return `Nothing`.
    """

    if value < 0:
        return option.Nothing()

    result = Zero()

    while value > 0:
        result = Succ(result)
        value -= 1

    return option.Some(result)


def from_builtin_int_exn(value: int) -> Nat:
    """
    Construct a `Nat` from a built-in `int`.

    Raises
    ------
    ValueError
        If `value` is negative.
    """

    match from_builtin_int(value):
        case option.Nothing():
            message = "argument must not be negative"
            raise ValueError(message)
        case option.Some(result):
            return result


@typing.overload
def by_ramp(value: typing.Literal[0]) -> Zero: ...
@typing.overload
def by_ramp(value: typing.Literal[1]) -> Succ[Zero]: ...
@typing.overload
def by_ramp(value: typing.Literal[2]) -> Succ[Succ[Zero]]: ...
@typing.overload
def by_ramp(value: typing.Literal[-1]) -> Zero: ...
@typing.overload
def by_ramp(value: int) -> Nat: ...


def by_ramp(value: int) -> Nat:
    """
    Construct a `Nat` value from a built-in `int` using the ramp
    function.

    If value is 0 or negative, the value returned will be `Zero`.
    If it is positive, it will be some `Succ`.
    """

    if value <= 0:
        return Zero()

    result = Zero()

    while value > 0:
        result = Succ(result)
        value -= 1

    return result


def length_of(container: collections.abc.Sized) -> Nat:
    """
    Return the length of `container`. It is exactly like the
    built-in function `len`, except that it returns a `Nat`.
    """

    return from_builtin_int_exn(len(container))
