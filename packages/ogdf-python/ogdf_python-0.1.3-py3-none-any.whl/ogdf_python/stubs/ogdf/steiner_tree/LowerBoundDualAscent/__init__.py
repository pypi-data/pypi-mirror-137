# file stubs/ogdf/steiner_tree/LowerBoundDualAscent/__init__.py generated from classogdf_1_1steiner__tree_1_1_lower_bound_dual_ascent
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class LowerBoundDualAscent(Generic[T]):

	"""Computes lower bounds for minimum Steiner tree instances."""

	@overload
	def __init__(self, graph : EdgeWeightedGraph[ T ], terminals : List[node], eps : float = 1e-6) -> None:
		"""Initializes the algorithm (and takes the first terminal as root)"""
		...

	@overload
	def __init__(self, graph : EdgeWeightedGraph[ T ], terminals : List[node], root : node, eps : float = 1e-6) -> None:
		"""Initializes the algorithm."""
		...

	def compute(self) -> None:
		"""Computes the lower bound."""
		...

	def get(self) -> T:
		"""Returns the lower bound."""
		...

	def reducedCost(self, adj : adjEntry) -> T:
		"""Returns the reduced cost of the arc given byadj."""
		...
