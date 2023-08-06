# file stubs/ogdf/steiner_tree/goemans/CoreEdgeRandomSpanningTree.py generated from classogdf_1_1steiner__tree_1_1goemans_1_1_core_edge_random_spanning_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class CoreEdgeRandomSpanningTree(ogdf.steiner_tree.goemans.CoreEdgeModule[ T ], Generic[T]):

	"""Computes a random set of core edges."""

	def __init__(self, rng : std.minstd_rand) -> None:
		...

	def call(self, graph : Graph, terminals : List[node], isInTree : EdgeArray[ bool ]) -> None:
		"""Compute a set of core edges."""
		...
