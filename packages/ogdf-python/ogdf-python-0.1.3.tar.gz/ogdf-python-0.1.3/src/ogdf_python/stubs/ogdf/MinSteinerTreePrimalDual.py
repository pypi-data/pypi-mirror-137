# file stubs/ogdf/MinSteinerTreePrimalDual.py generated from classogdf_1_1_min_steiner_tree_primal_dual
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreePrimalDual(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""Primal-Dual approximation algorithm for Steiner tree problems."""

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree given a weighted graph and a list of terminals."""
		...

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Calls the Steiner tree algorithm for nontrivial cases but handles trivial cases directly."""
		...

	def getLastLowerBound(self) -> float:
		"""Returns the lower bound calculated while solving the last problem."""
		...
