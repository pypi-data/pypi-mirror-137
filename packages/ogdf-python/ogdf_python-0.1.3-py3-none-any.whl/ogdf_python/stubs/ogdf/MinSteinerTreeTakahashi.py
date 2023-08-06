# file stubs/ogdf/MinSteinerTreeTakahashi.py generated from classogdf_1_1_min_steiner_tree_takahashi
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeTakahashi(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""This class implements the minimum Steiner tree 2-approximation algorithm by Takahashi and Matsuyama with improvements proposed by Poggi de Aragao et al."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], isOriginalTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""An extended call method with intermediate and final (original) terminals."""
		...

	@overload
	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], isOriginalTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ], startNode : node) -> T:
		"""An extended call method with intermediate and final (original) terminal nodes and a specific start node."""
		...

	@overload
	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ], startNode : node) -> T:
		"""An extended call method with specific start node."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Computes the actual Steiner tree."""
		...

	def terminalDijkstra(self, wG : EdgeWeightedGraph[ T ], intermediateTerminalSpanningTree : EdgeWeightedGraphCopy[ T ], s : node, numberOfTerminals : int, isTerminal : NodeArray[ bool ]) -> T:
		"""ModifiedDijkstraalgorithm to solve the Minimum Steiner Tree problem."""
		...
