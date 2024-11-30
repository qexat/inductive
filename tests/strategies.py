# noqa: D100, I002
from hypothesis import strategies

from inductive import nat

zeros = strategies.builds(nat.Zero)


def succs[N: nat.Nat](  # noqa: D103
    strategy: strategies.SearchStrategy[N],
) -> strategies.SearchStrategy[nat.Succ[N]]:
    return strategies.builds(nat.Succ[N], strategy)


nats: strategies.SearchStrategy[nat.Nat] = strategies.recursive(
    zeros,
    extend=succs,
    max_leaves=10_000,
)

nonzero_nats = nats.filter(lambda n: n != nat.zero)
