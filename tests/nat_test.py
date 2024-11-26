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


@given(nats)
def test_zero_less_than_n(n: nat.Nat) -> None:
    assert nat.zero < n


@given(nats)
def test_zero_less_equal_than_n(n: nat.Nat) -> None:
    assert nat.zero <= n


@given(nats)
def test_add_left_zero_elim(n: nat.Nat) -> None:
    assert nat.zero + n == n


@given(nats)
def test_add_right_zero_elim(n: nat.Nat) -> None:
    assert n + nat.zero == n


@given(nats)
def test_sub_zero_n_is_zero(n: nat.Nat) -> None:
    assert nat.zero - n == nat.zero


@given(nats)
def test_sub_n_zero_is_n(n: nat.Nat) -> None:
    assert n - nat.zero == n
