# file stubs/ogdf/MinSteinerTreeDualAscent.py generated from classogdf_1_1_min_steiner_tree_dual_ascent
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeDualAscent(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""Dual ascent heuristic for the minimum Steiner tree problem."""

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Creates a minimum Steiner tree given a weighted graph and a list of terminals."""
		...
