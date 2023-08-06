# file stubs/ogdf/SteinerTreeLowerBoundDualAscent.py generated from classogdf_1_1_steiner_tree_lower_bound_dual_ascent
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class SteinerTreeLowerBoundDualAscent(Generic[T]):

	"""Implementation of a dual-ascent-based lower bound heuristic for Steiner tree problems."""

	@overload
	def call(self, graph : EdgeWeightedGraph[ T ], terminals : List[node]) -> T:
		"""Calls the algorithm and returns the lower bound."""
		...

	@overload
	def call(self, graph : EdgeWeightedGraph[ T ], terminals : List[node], lbNodes : NodeArray[ T ], lbEdges : EdgeArray[ T ]) -> None:
		"""Compute the lower bounds under the assumption nodes or edges are included in the solution."""
		...

	def setRepetitions(self, num : int) -> None:
		"""Sets the number of repeated calls to the lower bound algorithm (runs with different roots)"""
		...
