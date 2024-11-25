"""
Utilitaries to configure the `inductive` library.
"""

from __future__ import annotations

import sys

__ORIGINAL_RECURSION_LIMIT = sys.getrecursionlimit()


def setup() -> None:
    """
    Modify the Python configuration to fit best the needs of
    this library.

    ⚠️ This alters values like the recursion limit. Use with
    extreme caution!
    """

    sys.setrecursionlimit(0x8000)


def teardown() -> None:
    """
    Restore the Python configuration to the state it was before
    `setup` was called.

    ⚠️ This OVERRIDES every change that happened in between!
    """

    sys.setrecursionlimit(__ORIGINAL_RECURSION_LIMIT)


class _InductiveContext:
    def __enter__(self) -> None:
        setup()

    def __exit__(self, *_: object) -> None:
        teardown()


def context() -> _InductiveContext:
    """
    Context manager that automatically calls the `setup` and
    `teardown` functions.
    """

    return _InductiveContext()
