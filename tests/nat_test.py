# ruff: noqa: PGH004
# ruff: noqa

# TODO: use composite strategies instead of `if` as it might not
# TODO: run the said tests at all!

from __future__ import annotations

from hypothesis import given
import option
from .strategies import nats, nonzero_nats

from inductive import config
from inductive import nat


def setup_module():
    config.setup()


def teardown_module():
    config.teardown()


# *- succ, pred -* #


# 1 = Succ(0)
def test_1_succ_0() -> None:
    assert nat.one == nat.succ(nat.zero)


# pred(0) = 0
def test_pred_0_0() -> None:
    assert nat.pred(nat.zero) == nat.zero


# ∀n : Nat, pred(succ(n)) == n
@given(nats)
def test_pred_succ_n_n(n: nat.Nat) -> None:
    assert nat.pred(nat.succ(n)) == n


# *- Comparison -* #


# ∀n : Nat, n == n
@given(nats)
def test_equality_reflexivity(n: nat.Nat) -> None:
    assert n == n


# ∀n m : Nat, n == m <-> m == n
@given(nats, nats)
def test_equality_symmetry(n: nat.Nat, m: nat.Nat) -> None:
    assert (n == m) == (m == n)


# ∀n m p : Nat, n == m -> m == p -> n == p
@given(nats, nats, nats)
def test_equality_transitivity(n: nat.Nat, m: nat.Nat, p: nat.Nat) -> None:
    # it's pretty bad, but assume() raises FailedHealthCheck
    if n == m and m == p:
        assert n == p


# ∀n : Nat, 0 > n == False
@given(nats)
def test_zero_greater_than_n_false(n: nat.Nat) -> None:
    assert (nat.zero > n) is False


# ∀n m : Nat, n == 0 -> m == 0 -> n > m
@given(nonzero_nats)
def test_nat_greater_zero(n: nat.Nat) -> None:
    assert n > nat.zero


# ∀n m : Nat, n == 0 -> m == 0 -> pred(n) > pred(m) <-> n > m
@given(nonzero_nats, nonzero_nats)
def test_nonzero_greater_than_nonzero_pred(n: nat.Nat, m: nat.Nat) -> None:
    assert (nat.pred(n) > nat.pred(m)) == (n > m)


# ∀n : Nat, n == 0 -> 0 >= n
def test_zero_greater_equal_zero() -> None:
    assert nat.zero >= nat.zero


# ∀n m : Nat, n == 0 -> m == 0 -> n >= m
@given(nonzero_nats)
def test_nat_greater_equal_zero(n: nat.Nat) -> None:
    assert n >= nat.zero


# ∀n m : Nat, n == 0 -> m == 0 -> pred(n) >= pred(m) <-> n >= m
@given(nonzero_nats, nonzero_nats)
def test_nonzero_greater_equal_nonzero_pred(n: nat.Nat, m: nat.Nat) -> None:
    assert (nat.pred(n) >= nat.pred(m)) == (n >= m)


# ∀n : Nat, n != 0 -> 0 >= n == False
@given(nonzero_nats)
def test_zero_greater_equal_nonzero_false(n: nat.Nat) -> None:
    assert (nat.zero >= n) is False


# ∀n : Nat, n != 0 -> 0 < n
@given(nonzero_nats)
def test_zero_less_than_nonzero(n: nat.Nat) -> None:
    assert nat.zero < n


# ∀n : Nat, 0 <= n
@given(nats)
def test_zero_less_equal_than_n(n: nat.Nat) -> None:
    assert nat.zero <= n


# ∀n m : Nat, n <= m -> n < Succ(m)
@given(nats, nats)
def test_le_n_lt_succ_n(n: nat.Nat, m: nat.Nat) -> None:
    assert (n <= m) == (n < nat.Succ(m))


# *- Arithmetic -* #


# ∀n : Nat, 0 + n == n
@given(nats)
def test_add_left_zero_elim(n: nat.Nat) -> None:
    assert nat.zero + n == n


# ∀n : Nat, n + 0 == n
@given(nats)
def test_add_right_zero_elim(n: nat.Nat) -> None:
    assert n + nat.zero == n


# ∀n m : Nat, Succ(n) + m == Succ(n + m)
@given(nats, nats)
def test_add_succ_left(n: nat.Nat, m: nat.Nat) -> None:
    assert nat.Succ(n) + m == nat.Succ(n + m)


# ∀n m : Nat, n + m == m + n
@given(nats, nats)
def test_add_commutativity(n: nat.Nat, m: nat.Nat) -> None:
    assert n + m == m + n


# ∀n m p : Nat, (n + m) + p == n + (m + p)
@given(nats, nats, nats)
def test_add_associativity(n: nat.Nat, m: nat.Nat, p: nat.Nat) -> None:
    assert (n + m) + p == n + (m + p)


# ∀n : Nat, 0 - n == 0
@given(nats)
def test_sub_zero_n_is_zero(n: nat.Nat) -> None:
    assert nat.zero - n == nat.zero


# ∀n : Nat, n - 0 == n
@given(nats)
def test_sub_n_zero_is_n(n: nat.Nat) -> None:
    assert n - nat.zero == n


# ∀n m : Nat, n - Succ(m) == pred(n - m)
@given(nats, nats)
def test_sub_pred_right(n: nat.Nat, m: nat.Nat) -> None:
    assert n - nat.Succ(m) == nat.pred(n - m)


# ∀n m p: Nat, n - (m + p) == n - m - p
@given(nats, nats, nats)
def test_sub_add_distributivity(n: nat.Nat, m: nat.Nat, p: nat.Nat) -> None:
    assert n - (m + p) == n - m - p


# ∀n m p: Nat, n - (m - p) == n - m + p
@given(nats, nats, nats)
def test_sub_sub_distributivity(n: nat.Nat, m: nat.Nat, p: nat.Nat) -> None:
    if p <= m and m <= n:
        assert n - (m - p) == n - m + p


# ∀n : Nat, 0 * n == 0
@given(nats)
def test_mul_zero_left(n: nat.Nat) -> None:
    assert nat.zero * n == nat.zero


# ∀n : Nat, n * 0 == 0
@given(nats)
def test_mul_zero_right(n: nat.Nat) -> None:
    assert n * nat.zero == nat.zero


# ∀n : Nat, 1 * n == n
@given(nats)
def test_mul_identity_left(n: nat.Nat) -> None:
    assert nat.one * n == n


# ∀n : Nat, n * 1 == n
@given(nats)
def test_mul_identity_right(n: nat.Nat) -> None:
    assert n * nat.one == n


# ∀n m : Nat, n * m == m * n
@given(nats, nats)
def test_mul_commutativity(n: nat.Nat, m: nat.Nat) -> None:
    assert n * m == m * n


# ∀n m p : Nat, (n * m) * p == n * (m * p)
@given(nats, nats, nats)
def test_mul_associativity(n: nat.Nat, m: nat.Nat, p: nat.Nat) -> None:
    assert (n * m) * p == n * (m * p)


# ∀n m p : Nat, n * (m + p) == n * m + n * p
@given(nats, nats, nats)
def test_mul_add_distributivity_left(
    n: nat.Nat,
    m: nat.Nat,
    p: nat.Nat,
) -> None:
    assert n * (m + p) == n * m + n * p


# ∀n m p : Nat, (n + m) * p == n * p + m * p
@given(nats, nats, nats)
def test_mul_add_distributivity_right(
    n: nat.Nat,
    m: nat.Nat,
    p: nat.Nat,
) -> None:
    assert (n + m) * p == n * p + m * p


# ∀n m p : Nat, n * (m - p) == n * m - n * p
@given(nats, nats, nats)
def test_mul_sub_distributivity_left(
    n: nat.Nat,
    m: nat.Nat,
    p: nat.Nat,
) -> None:
    assert n * (m - p) == n * m - n * p


# ∀n m p : Nat, (n - m) * p == n * p - m * p
@given(nats, nats, nats)
def test_mul_sub_distributivity_right(
    n: nat.Nat,
    m: nat.Nat,
    p: nat.Nat,
) -> None:
    assert (n - m) * p == n * p - m * p


# ∀n: Nat, n == 0 -> divmod(0, n) == Nothing()
def test_divmod_zero_zero() -> None:
    assert divmod(nat.zero, nat.zero) == option.Nothing()


# ∀n : Nat, n != 0 -> divmod(0, n) == Some((0, 0))
@given(nonzero_nats)
def test_divmod_zero_nonzero(n: nat.Nat) -> None:
    assert divmod(nat.zero, n) == option.Some((nat.zero, nat.zero))


# ∀n : Nat, divmod(n, 0) == Nothing()
@given(nats)
def test_divmod_n_zero(n: nat.Nat) -> None:
    assert divmod(n, nat.zero) == option.Nothing()


# ∀n : Nat, divmod(n, 1) == Some((n, 0))
@given(nats)
def test_divmod_n_one(n: nat.Nat) -> None:
    assert divmod(n, nat.one) == option.Some((n, nat.zero))


# ∀n : Nat, n == 0 -> 0 / n == Nothing()
def test_truediv_zero_zero() -> None:
    assert nat.zero / nat.zero == option.Nothing()


# ∀n : Nat, n != 0 -> 0 / n == Some(0)
@given(nonzero_nats)
def test_truediv_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero / n == option.Some(nat.zero)


# ∀n m : Nat, n != 0 -> m == 0 -> n / m == Nothing()
@given(nonzero_nats)
def test_truediv_nonzero_zero(n: nat.Nat) -> None:
    assert n / nat.zero == option.Nothing()


# ∀n m : Nat, n != 0 -> m != 0 -> (n / m : Some)
@given(nonzero_nats, nonzero_nats)
def test_truediv_nonzero_nonzero(n: nat.Nat, m: nat.Nat) -> None:
    assert isinstance(n / m, option.Some)


# ∀n : Nat, n == 0 -> 0 // n == 0
def test_floordiv_zero_zero() -> None:
    assert nat.zero // nat.zero == nat.zero


# ∀n : Nat, n != 0 -> 0 // n == 0
@given(nonzero_nats)
def test_floordiv_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero // n == nat.zero


# ∀n : Nat, n != 0 -> n // 0 == 0
@given(nonzero_nats)
def test_floordiv_nonzero_zero(n: nat.Nat) -> None:
    assert (n // nat.zero) == nat.zero


# ∀n : Nat, n != 0 -> n // n == 1
@given(nonzero_nats)
def test_floordiv_nonzero_identity(n: nat.Nat) -> None:
    assert (n // n) == nat.one


# ∀n m : Nat, n != 0 -> m != 0 -> n < m -> n // m == 0
@given(nonzero_nats, nonzero_nats)
def test_floordiv_nonzero_nonzero_less(n: nat.Nat, m: nat.Nat) -> None:
    if n < m:
        assert (n // m) == nat.zero


# ∀n m : Nat, n != 0 -> m != 0 -> n == m -> n // m == 1
@given(nonzero_nats, nonzero_nats)
def test_floordiv_nonzero_nonzero_equal(n: nat.Nat, m: nat.Nat) -> None:
    if n == m:
        assert (n // m) == nat.one


# ∀n m : Nat, n != 0 -> m != 0 -> n > m -> n // m >= 1
@given(nonzero_nats, nonzero_nats)
def test_floordiv_nonzero_nonzero_greater(n: nat.Nat, m: nat.Nat) -> None:
    if n > m:
        assert (n // m) >= nat.one


# ∀n : Nat, n == 0 -> 0 % n == 0
def test_mod_zero_zero() -> None:
    assert nat.zero % nat.zero == nat.zero


# ∀n : Nat, n != 0 -> 0 % n == 0
@given(nonzero_nats)
def test_mod_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero % n == nat.zero


# ∀n m : Nat, n != 0 -> m == 0 -> n % m == 0
@given(nonzero_nats)
def test_mod_nonzero_zero(n: nat.Nat) -> None:
    assert n % nat.zero == nat.zero


# ∀n m : Nat, n != 0 -> m != 0 -> n < m -> n % m == n
@given(nonzero_nats, nonzero_nats)
def test_mod_nonzero_nonzero_less(n: nat.Nat, m: nat.Nat) -> None:
    if n < m:
        assert n % m == n


# ∀n m : Nat, n != 0 -> m != 0 -> n == m -> n % m == 0
@given(nonzero_nats, nonzero_nats)
def test_mod_nonzero_nonzero_equal(n: nat.Nat, m: nat.Nat) -> None:
    if n == m:
        assert n % m == nat.zero


# ∀n m : Nat, n != 0 -> m != 0 -> n % m < m
@given(nonzero_nats, nonzero_nats)
def test_mod_nonzero_nonzero_cycle(n: nat.Nat, m: nat.Nat) -> None:
    assert n % m < m


# ∀n : Nat, abs(n) == n
@given(nats)
def test_abs_nonzero(n: nat.Nat) -> None:
    assert abs(n) == n


# bool(0) == False
def test_bool_zero() -> None:
    assert bool(nat.zero) is False


# ∀n : Nat, n != 0 -> bool(n)
@given(nonzero_nats)
def test_bool_nonzero(n: nat.Nat) -> None:
    assert bool(n) is True


# complex(0) == 0j
def test_complex_zero() -> None:
    assert complex(nat.zero) == 0j


# ∀n : Nat, complex(n) == float(n) + 0j
@given(nats)
def test_complex_n_float(n: nat.Nat) -> None:
    assert complex(n) == float(n) + 0j


# ∀n : Nat, complex(n) == int(n) + 0j
@given(nats)
def test_complex_n_int(n: nat.Nat) -> None:
    assert complex(n) == int(n) + 0j


# float(0) == 0.0
def test_float_zero() -> None:
    assert float(nat.zero) == 0.0


# ∀n m : Nat, n < m <-> float(n) < float(m)
@given(nats, nats)
def test_float_order_preservation(n: nat.Nat, m: nat.Nat) -> None:
    assert (n < m) == (float(n) < float(m))


# int(0) == 0
def test_int_zero() -> None:
    assert int(nat.zero) == 0


# ∀n m : Nat, n == m <-> int(n) == int(m)
@given(nats, nats)
def test_int_bijective(n: nat.Nat, m: nat.Nat) -> None:
    assert (n == m) == (int(n) == int(m))


# str(0) == "0"
def test_str_zero() -> None:
    assert str(nat.zero) == "0"


# str(1) == "1"
def test_str_one() -> None:
    assert str(nat.one) == "1"


# str(2) == "2"
def test_str_two() -> None:
    assert str(nat.two) == "2"


# str(3) == "3"
def test_str_three() -> None:
    assert str(nat.three) == "3"


# str(4) == "4"
def test_str_four() -> None:
    assert str(nat.four) == "4"


# str(5) == "5"
def test_str_five() -> None:
    assert str(nat.five) == "5"


# str(6) == "6"
def test_str_six() -> None:
    assert str(nat.six) == "6"


# str(7) == "7"
def test_str_seven() -> None:
    assert str(nat.seven) == "7"


# str(8) == "8"
def test_str_eight() -> None:
    assert str(nat.eight) == "8"


# str(9) == "9"
def test_str_nine() -> None:
    assert str(nat.nine) == "9"


# str(10) == "10"
def test_str_ten() -> None:
    assert str(nat.ten) == "10"


# ∀n m : Nat, n == m <-> str(n) == str(m)
@given(nats, nats)
def test_str_bijective(n: nat.Nat, m: nat.Nat) -> None:
    assert (n == m) == (str(n) == str(m))


# ∀n : Nat, int(str(n)) == int(n)
@given(nats)
def test_int_str_int(n: nat.Nat) -> None:
    assert int(str(n)) == int(n)


# repr(0) == "Zero"
def test_repr_zero() -> None:
    assert repr(nat.zero) == "Zero"


# ∀n : Nat, n != 0 -> repr(n) == "Succ(" + repr(pred(n)) + ")"
@given(nonzero_nats)
def test_repr_inductive(n: nat.Nat) -> None:
    assert repr(n) == f"Succ({repr(nat.pred(n))})"


# bytes(0) == b""
def test_bytes_zero() -> None:
    assert bytes(nat.zero) == b""


# ∀n : Nat, length_of(bytes(n)) == n
@given(nats)
def test_length_of_bytes_n(n: nat.Nat) -> None:
    assert nat.length_of(bytes(n)) == n


# ∀n : Nat, n == 0 -> n.double() == 0
def test_double_zero() -> None:
    assert nat.zero.double() == nat.zero


# ∀n : Nat, n != 0 -> n.double() > n
@given(nonzero_nats)
def test_double_nonzero(n: nat.Nat) -> None:
    assert n.double() > n


# ∀n : Nat, n == 0 -> n.square() == 0
def test_square_zero() -> None:
    assert nat.zero.square() == nat.zero


# ∀n : Nat, n == 1 -> n.square() == 1
def test_square_one() -> None:
    assert nat.one.square() == nat.one


# ∀n : Nat, n > 1 -> n.square() > n
@given(nats.filter(lambda n: n > nat.one))
def test_square_nonzero(n: nat.Nat) -> None:
    assert n.square() > n


# ∀n : Nat, n == 0 -> n.is_odd() == False
def test_is_odd_zero() -> None:
    assert nat.zero.is_odd() is False


# ∀n : Nat, n != 0 -> n.is_odd() == not pred(n).is_odd()
@given(nonzero_nats)
def test_is_odd_nonzero_not_pred(n: nat.Nat) -> None:
    assert n.is_odd() == (not nat.pred(n).is_odd())


# ∀n : Nat, n == 0 -> n.is_even() == False
def test_is_even_zero() -> None:
    assert nat.zero.is_even() is True


# ∀n : Nat, n != 0 -> n.is_even() == not pred(n).is_even()
@given(nonzero_nats)
def test_is_even_nonzero_not_pred(n: nat.Nat) -> None:
    assert n.is_even() == (not nat.pred(n).is_even())


# ∀n : Nat, n == 0 -> n.as_integer_ratio() == (0, 1)
def test_as_integer_ratio_zero() -> None:
    assert nat.zero.as_integer_ratio() == (0, 1)


# ∀n : Nat, n != 0 -> n.as_integer_ratio() == (int(n), 1)
@given(nonzero_nats)
def test_as_integer_ratio_nonzero(n: nat.Nat) -> None:
    assert n.as_integer_ratio() == (int(n), 1)
