# file stubs/ogdf/MinSteinerTreeRZLoss/__init__.py generated from classogdf_1_1_min_steiner_tree_r_z_loss
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeRZLoss(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""This class implements the loss-contracting (1.55+epsilon)-approximation algorithm for the Steiner tree problem by Robins and Zelikovsky."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, v : int) -> None:
		...

	def __destruct__(self) -> None:
		...

	def numberOfComponentLookUps(self) -> int:
		"""Returns the number of components lookups during execution time."""
		...

	def numberOfContractedComponents(self) -> int:
		"""Returns the number of contracted components."""
		...

	def numberOfGeneratedComponents(self) -> int:
		"""Returns the number of generated components."""
		...

	def setMaxComponentSize(self, k : int) -> None:
		"""Sets the maximal number of terminals in a full component."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree given a weighted graph and a list of terminals."""
		...
