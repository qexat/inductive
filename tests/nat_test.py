# ruff: noqa: PGH004
# ruff: noqa

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


# *- Succ, pred -* #


# 1 = Succ(0)
def test_1_succ_0() -> None:
    assert nat.one == nat.Succ(nat.zero)


# pred(0) = 0
def test_pred_0_0() -> None:
    assert nat.pred(nat.zero) == nat.zero


# ∀n : Nat, pred(Succ(n)) == n
@given(nats)
def test_pred_succ_n_n(n: nat.Nat) -> None:
    assert nat.pred(nat.Succ(n)) == n


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


# TODO: - nonzero // zero
#       - nonzero // nonzero


# ∀n : Nat, n == 0 -> 0 % n == 0
def test_mod_zero_zero() -> None:
    assert nat.zero % nat.zero == nat.zero


# ∀n : Nat, n != 0 -> 0 % n == 0
@given(nonzero_nats)
def test_mod_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero % n == nat.zero


# TODO: - nonzero % zero
#       - nonzero % nonzero


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
