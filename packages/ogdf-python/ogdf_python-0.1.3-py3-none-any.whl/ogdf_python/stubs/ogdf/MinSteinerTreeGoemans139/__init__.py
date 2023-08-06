# file stubs/ogdf/MinSteinerTreeGoemans139/__init__.py generated from classogdf_1_1_min_steiner_tree_goemans139
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeGoemans139(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""This class implements the (1.39+epsilon)-approximation algorithm for the Steiner tree problem by Goemans et."""

	m_preprocess : bool = ...

	m_restricted : int = ...

	m_seed : int = ...

	m_separateCycles : bool = ...

	m_use2approx : bool = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def disablePreprocessing(self, preprocess : bool = True) -> None:
		"""Disable preprocessing of LP solutions."""
		...

	def separateCycles(self, separateCycles : bool = True) -> None:
		"""Use stronger LP relaxation (not recommended in general)"""
		...

	def setMaxComponentSize(self, k : int) -> None:
		"""Sets the maximal number of terminals in a full component."""
		...

	def setSeed(self, seed : int) -> None:
		"""Set seed for the random number generation."""
		...

	def use2Approximation(self, use2approx : bool = True) -> None:
		"""Use Takahashi-Matsuyama 2-approximation as upper bounds."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree for a given weighted graph with terminals."""
		...
