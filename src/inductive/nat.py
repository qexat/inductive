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

if typing.TYPE_CHECKING:
    import collections.abc


@attrs.frozen
@typing.final
class Zero:
    """
    `Zero` represents the number 0.
    """

    # *- Comparison -* #
    # equality is handled by attrs

    # forall n : Nat, 0 > n = False
    def __gt__(self, other: Nat, /) -> typing.Literal[False]:
        return False

    # forall n : Nat, 0 >= n = False
    def __ge__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return False

    # forall n : Nat, n == 0 -> 0 < n = False
    # forall n : Nat, n != 0 -> 0 < n
    def __lt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return True

    # forall n : Nat, 0 <= n
    def __le__(self, other: Nat, /) -> typing.Literal[True]:
        return True

    # *- Arithmetic -* #

    # forall n : Nat, 0 + n = n
    def __add__[N: Nat](self, other: N, /) -> N:
        return other

    # forall n : nat, n + 0 = n
    def __radd__[N: Nat](self, other: N, /) -> N:
        return other

    # forall n : nat, 0 - n = 0
    def __sub__(self, other: Nat, /) -> Zero:
        return self

    # forall n : nat, n - 0 = n
    def __rsub__[N: Nat](self, other: N, /) -> N:
        return other

    # forall n : nat, 0 * n = 0
    def __mul__(self, other: Nat, /) -> Zero:
        return self

    # forall n : nat, n * 0 = 0
    def __rmul__(self, other: Nat, /) -> Zero:
        return self

    # We implement divmod for completeness
    def __divmod__(self, other: Nat, /) -> option.Option[tuple[Zero, Zero]]:
        match other:
            case Zero():
                return option.Nothing()
            case Succ():
                return option.Some((Zero(), Zero()))

    # forall n : nat, n == 0 -> 0 / n = Nothing
    # forall n : nat, n != 0 -> 0 / n = Some(0)
    def __truediv__(self, other: Nat, /) -> option.Option[Zero]:
        match other:
            case Zero():
                return option.Nothing()
            case Succ():
                return option.Some(self)

    # forall n : nat, n / 0 = Nothing
    def __rtruediv__(self, other: Nat, /) -> option.Nothing:
        return option.Nothing()

    # forall n : nat, n == 0 -> 0 // n = 0
    # forall n : nat, n != 0 -> 0 // n = 0
    def __floordiv__(self, other: Nat, /) -> Zero:
        return self

    # forall n : nat, n // 0 = 0
    def __rfloordiv__(self, other: Nat, /) -> Zero:
        return self

    # forall n : nat, n == 0 -> 0 % n = 0
    # forall n : nat, n != 0 -> 0 % n = 0
    def __mod__(self, other: Nat, /) -> Zero:
        return self

    # forall n : nat, n % 0 = 0
    def __rmod__(self, other: Nat, /) -> Zero:
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

    def __iter__(self) -> collections.abc.Generator[Nat]:
        n = self

        while n > zero:
            yield n
            n = pred(n)

        yield n


@attrs.frozen
@typing.final
class Succ[N: Nat]:
    """
    `Succ[N]` represents the next number after `N`.
    """

    predecessor: N

    # *- Comparison -* #
    # equality is handled by attrs

    # forall n m : Nat, m == 0 -> Succ(n) > m
    # forall n m : Nat, m != 0 -> n > m -> Succ(n) > Succ(m)
    def __gt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return self.predecessor > other.predecessor

    # forall n m : Nat, m == 0 -> Succ(n) >= m
    # forall n m : Nat, m != 0 -> n >= m -> Succ(n) >= Succ(m)
    def __ge__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return True
            case Succ():
                return self.predecessor >= other.predecessor

    # forall n m : Nat, m == 0 -> Succ(m) < 0 = False
    # forall n m : Nat, m != 0 -> n < m -> Succ(n) < Succ(m)
    def __lt__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return self.predecessor < other.predecessor

    # forall n m : Nat, m == 0 -> Succ(m) < 0 = False
    # forall n m : Nat, m != 0 -> n <= m -> Succ(n) <= Succ(m)
    def __le__(self, other: Nat, /) -> bool:
        match other:
            case Zero():
                return False
            case Succ():
                return self.predecessor <= other.predecessor

    # *- Arithmetic -* #

    # forall n m : Nat, m == 0 -> n + m = n
    # forall n m : Nat, m != 0 -> n + m = succ(n) + pred(m)
    def __add__(self, other: Nat, /) -> typing.Self | Nat:
        match other:
            case Zero():
                return self
            case Succ():
                # XXX: Pyright fails to infer the type of that
                return Succ(self) + other.predecessor  # pyright: ignore[reportArgumentType, reportUnknownVariableType]

    # forall n m : nat, m == 0 -> n - m = n
    # forall n m : nat, m != 0 -> n - m = Succ(n) - Succ(m)
    def __sub__(self, other: Nat, /) -> typing.Self | Nat:
        match other:
            case Zero():
                return self
            case Succ():
                return self.predecessor - other.predecessor

    # forall n m : nat, m == 0 -> n * m = 0
    # forall n m : nat, m != 0 -> n + (n * pred(m))
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
        return (1 + 0j) + complex(self.predecessor)  # pyright: ignore[reportArgumentType, reportCallIssue]

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
        predecessor_repr = "..." if self > five else repr(self.predecessor)

        return f"Succ({predecessor_repr})"

    def __bytes__(self) -> bytes:
        return b"\x00" + bytes(self.predecessor)  # pyright: ignore[reportArgumentType]


type Nat = Zero | Succ[Nat]

# *- Digits -* #

zero = Zero()
one = Succ(Zero())
two = Succ(one)
three = Succ(two)
four = Succ(three)
five = Succ(four)
six = Succ(five)
seven = Succ(six)
eight = Succ(seven)
nine = Succ(eight)
ten = Succ(nine)

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


def double(n: Nat) -> Nat:
    """
    Return the double of `n`.
    """

    return n + n


def square(n: Nat) -> Nat:
    """
    Return the square of `n`.
    """

    return n * n


def ramp(n: Nat) -> Nat:
    """
    Return `max(0, n)`.

    Since `n` is always greater or equal to 0, this function is
    essentially a no-op.
    """

    return n


def ramp_inverse(_: Nat) -> Zero:
    """
    Return `min(0, n)`.

    Since `n` is always greater or equal to 0, this function
    returns 0.
    """

    return Zero()


def is_odd(n: Nat) -> bool:
    """
    Return whether `n` is odd.
    """

    result = False

    while n > zero:
        n = pred(n)
        result = not result

    return result


def is_even(n: Nat) -> bool:
    """
    Return whether `n` is even.
    """

    result = True

    while n > zero:
        n = pred(n)
        result = not result

    return result


def as_integer_ratio(n: Nat) -> tuple[int, typing.Literal[1]]:
    """
    Return a pair of integers, whose ratio is equal to the original int.

    The ratio is in lowest terms and has a positive denominator.
    """

    return (int(n), 1)


# *- Constructors from built-in integers -* #


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
