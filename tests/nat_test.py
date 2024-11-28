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


# ∀n : Nat, 0 > n == False
@given(nats)
def test_zero_greater_than_n_false(n: nat.Nat) -> None:
    assert (nat.zero > n) is False


# ∀n : Nat, n == 0 -> 0 >= n
def test_zero_greater_equal_zero() -> None:
    assert nat.zero >= nat.zero


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


# ∀n m : nat, n <= m -> n < Succ(m)
@given(nats, nats)
def test_le_n_lt_succ_n(n: nat.Nat, m: nat.Nat) -> None:
    assert (n <= m) == (n < nat.Succ(m))


# *- Arithmetic -* #


# ∀n : nat, 0 + n == n
@given(nats)
def test_add_left_zero_elim(n: nat.Nat) -> None:
    assert nat.zero + n == n


# ∀n : nat, n + 0 == n
@given(nats)
def test_add_right_zero_elim(n: nat.Nat) -> None:
    assert n + nat.zero == n


# ∀n m : nat, Succ(n) + m == Succ(n + m)
@given(nats, nats)
def test_add_succ_left(n: nat.Nat, m: nat.Nat) -> None:
    assert nat.Succ(n) + m == nat.Succ(n + m)


# ∀n : nat, 0 - n == 0
@given(nats)
def test_sub_zero_n_is_zero(n: nat.Nat) -> None:
    assert nat.zero - n == nat.zero


# ∀n : nat, n - 0 == n
@given(nats)
def test_sub_n_zero_is_n(n: nat.Nat) -> None:
    assert n - nat.zero == n


# ∀n m : nat, n - Succ(m) == pred(n - m)
@given(nats, nats)
def test_sub_pred_right(n: nat.Nat, m: nat.Nat) -> None:
    assert n - nat.Succ(m) == nat.pred(n - m)


# ∀n : nat, 0 * n == 0
@given(nats)
def test_mul_zero_left(n: nat.Nat) -> None:
    assert nat.zero * n == nat.zero


# ∀n: nat, n == 0 -> divmod(0, n) == Nothing()
def test_divmod_zero_zero() -> None:
    assert divmod(nat.zero, nat.zero) == option.Nothing()


# ∀n : nat, n != 0 -> divmod(0, n) == Some((0, 0))
@given(nonzero_nats)
def test_divmod_zero_nonzero(n: nat.Nat) -> None:
    assert divmod(nat.zero, n) == option.Some((nat.zero, nat.zero))


# ∀n : nat, n == 0 -> 0 / n == Nothing()
def test_truediv_zero_zero() -> None:
    assert nat.zero / nat.zero == option.Nothing()


# ∀n : nat, n != 0 -> 0 / n == Some(0)
@given(nonzero_nats)
def test_truediv_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero / n == option.Some(nat.zero)


# ∀n : nat, n == 0 -> 0 // n == 0
def test_floordiv_zero_zero() -> None:
    assert nat.zero // nat.zero == nat.zero


# ∀n : nat, n != 0 -> 0 // n == 0
@given(nonzero_nats)
def test_floordiv_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero // n == nat.zero


# ∀n : nat, n == 0 -> 0 % n == 0
def test_mod_zero_zero() -> None:
    assert nat.zero % nat.zero == nat.zero


# ∀n : nat, n != 0 -> 0 % n == 0
@given(nonzero_nats)
def test_mod_zero_nonzero(n: nat.Nat) -> None:
    assert nat.zero % n == nat.zero


def test_abs_zero() -> None:
    assert abs(nat.zero) == nat.zero


def test_bool_zero() -> None:
    assert bool(nat.zero) is False


def test_complex_zero() -> None:
    assert complex(nat.zero) == 0j


def test_float_zero() -> None:
    assert float(nat.zero) == 0.0


def test_int_zero() -> None:
    assert int(nat.zero) == 0


def test_str_zero() -> None:
    assert str(nat.zero) == "0"


def test_repr_zero() -> None:
    assert repr(nat.zero) == "Zero"


def test_bytes_zero() -> None:
    assert bytes(nat.zero) == b""
