# file stubs/ogdf/CoffmanGrahamRanking/__init__.py generated from classogdf_1_1_coffman_graham_ranking
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CoffmanGrahamRanking(ogdf.RankingModule):

	"""The coffman graham ranking algorithm."""

	# Algorithm call

	def call(self, G : Graph, rank : NodeArray[  int ]) -> None:
		"""Computes a node ranking ofGinrank."""
		...

	# Module options

	def setSubgraph(self, pSubgraph : AcyclicSubgraphModule) -> None:
		"""Sets the module for the computation of the acyclic subgraph."""
		...

	def __init__(self) -> None:
		"""Creates an instance of coffman graham ranking."""
		...

	@overload
	def width(self) -> int:
		"""Get for the with."""
		...

	@overload
	def width(self, w : int) -> None:
		"""Set for the with."""
		...
