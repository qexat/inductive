"""
# inductive

`inductive` is a library that defines inductive data structures
such as Peano numbers and linked lists.

It is recommended to call the `setup()` function before usage.
"""

from . import nat
from .config import context
from .config import setup
from .config import teardown

__all__ = ["context", "nat", "setup", "teardown"]
