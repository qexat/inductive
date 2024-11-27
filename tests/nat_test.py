# ruff: noqa: PGH004
# ruff: noqa

from __future__ import annotations

from hypothesis import given
from .strategies import nats

from inductive import config
from inductive import nat


def setup_module():
    config.setup()


def teardown_module():
    config.teardown()


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


# ∀n : Nat, n != 0 -> 0 < n
@given(nats.filter(lambda n: n != nat.zero))
def test_zero_less_than_n(n: nat.Nat) -> None:
    assert nat.zero < n


# ∀n : Nat, 0 <= n
@given(nats)
def test_zero_less_equal_than_n(n: nat.Nat) -> None:
    assert nat.zero <= n


# ∀n m : nat, n <= m -> n < Succ(m)
@given(nats, nats)
def test_le_n_lt_succ_n(n: nat.Nat, m: nat.Nat) -> None:
    assert (n <= m) == (n < nat.Succ(m))


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
