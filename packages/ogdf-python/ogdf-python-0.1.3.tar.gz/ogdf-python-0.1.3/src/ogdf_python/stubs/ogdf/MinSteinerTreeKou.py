# file stubs/ogdf/MinSteinerTreeKou.py generated from classogdf_1_1_min_steiner_tree_kou
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeKou(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""This class implements the Minimum Steiner Tree 2-approximation algorithm by Kou et al."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def calculateCompleteGraph(self, wG : EdgeWeightedGraph[ T ], terminals : List[node], predecessor : EdgeArray[List[edge]], completeTerminalGraph : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Builds a complete terminal graph."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree given a weighted graph and a list of terminals."""
		...

	def insertPath(self, ssspPred : List[edge], finalSteinerTree : EdgeWeightedGraphCopy[ T ], wG : EdgeWeightedGraph[ T ]) -> None:
		"""Inserts a shortest path corresponding to an edge in the complete terminal graph."""
		...

	def reinsertShortestPaths(self, completeTerminalGraph : EdgeWeightedGraphCopy[ T ], ssspPred : EdgeArray[List[edge]], mstPred : NodeArray[edge], finalSteinerTree : EdgeWeightedGraphCopy[ T ], wG : EdgeWeightedGraph[ T ]) -> None:
		"""Swaps an edge in the complete terminal graph with the corresponding shortest path in the original graph."""
		...
