# noqa: A005, I002
"""
`inductive.builtins` re-exports some symbols from the other
parts of `inductive` that are meant to replace some built-ins.

For example, `length` replaces `len` for containers that aren't
defined in this library - otherwise, simply use the `.length`
method.
"""

from .nat import length_of as length

__all__ = ["length"]
