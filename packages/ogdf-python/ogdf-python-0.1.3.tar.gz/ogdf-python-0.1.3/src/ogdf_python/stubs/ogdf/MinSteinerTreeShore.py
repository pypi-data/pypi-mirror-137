# file stubs/ogdf/MinSteinerTreeShore.py generated from classogdf_1_1_min_steiner_tree_shore
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeShore(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""Implementation of Shore, Foulds and Gibbons exact branch and bound algorithm for solving Steiner tree problems."""

	MAX_WEIGHT : T = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree given a weighted graph and a list of terminals."""
		...
