# file stubs/ogdf/steiner_tree/goemans/Approximation/__init__.py generated from classogdf_1_1steiner__tree_1_1goemans_1_1_approximation
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Approximation(Generic[T]):

	"""The actual 1.39-approximation algorithm by Goemans et al. with a set of terminalized nodes as result."""

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], fullCompStore : FullComponentWithExtraStore[ T, float ], rng : std.minstd_rand, eps : float = 1e-8) -> None:
		"""Initialize everything."""
		...

	def solve(self, isNewTerminal : NodeArray[ bool ]) -> None:
		"""Perform the actual approximation algorithm on the LP solution."""
		...
