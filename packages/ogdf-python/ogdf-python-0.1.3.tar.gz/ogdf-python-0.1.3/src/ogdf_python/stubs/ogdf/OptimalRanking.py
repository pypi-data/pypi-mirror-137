# file stubs/ogdf/OptimalRanking.py generated from classogdf_1_1_optimal_ranking
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OptimalRanking(ogdf.RankingModule):

	"""The optimal ranking algorithm."""

	# Algorithm call

	@overload
	def call(self, G : Graph, rank : NodeArray[  int ]) -> None:
		"""Computes a node ranking ofGinrank."""
		...

	@overload
	def call(self, G : Graph, length : EdgeArray[  int ], rank : NodeArray[  int ]) -> None:
		"""Computes a node ranking ofGwith given minimal edge length inrank."""
		...

	@overload
	def call(self, G : Graph, length : EdgeArray[  int ], cost : EdgeArray[  int ], rank : NodeArray[  int ]) -> None:
		"""Computes a cost-minimal node ranking ofGfor given edge costs and minimal edge lengths inrank."""
		...

	# Optional parameters

	@overload
	def separateMultiEdges(self) -> bool:
		"""Returns the current setting of option separateMultiEdges."""
		...

	@overload
	def separateMultiEdges(self, b : bool) -> None:
		"""Sets the option separateMultiEdges tob."""
		...

	# Module options

	def setSubgraph(self, pSubgraph : AcyclicSubgraphModule) -> None:
		"""Sets the module for the computation of the acyclic subgraph."""
		...

	def __init__(self) -> None:
		"""Creates an instance of optimal ranking."""
		...
