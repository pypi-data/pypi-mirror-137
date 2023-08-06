# file stubs/ogdf/LongestPathRanking.py generated from classogdf_1_1_longest_path_ranking
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LongestPathRanking(ogdf.RankingModule):

	"""The longest-path ranking algorithm."""

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
		"""Computes a node ranking ofGwith given minimal edge length inrank."""
		...

	def callUML(self, AG : GraphAttributes, rank : NodeArray[  int ]) -> None:
		"""Call for UML graphs with special treatement of inheritance hierarchies."""
		...

	# Optional parameters

	@overload
	def separateDeg0Layer(self) -> bool:
		"""Returns the current setting of option separateDeg0Layer."""
		...

	@overload
	def separateDeg0Layer(self, sdl : bool) -> None:
		"""Sets the option separateDeg0Layer tosdl."""
		...

	@overload
	def separateMultiEdges(self) -> bool:
		"""Returns the current setting of option separateMultiEdges."""
		...

	@overload
	def separateMultiEdges(self, b : bool) -> None:
		"""Sets the option separateMultiEdges tob."""
		...

	@overload
	def optimizeEdgeLength(self) -> bool:
		"""Returns the current setting of option optimizeEdgeLength."""
		...

	@overload
	def optimizeEdgeLength(self, b : bool) -> None:
		"""Sets the option optimizeEdgeLength tob."""
		...

	@overload
	def alignBaseClasses(self) -> bool:
		"""Returns the current setting of alignment of base classes (callUML only)."""
		...

	@overload
	def alignBaseClasses(self, b : bool) -> None:
		"""Sets the option for alignment of base classes tob."""
		...

	@overload
	def alignSiblings(self) -> bool:
		"""Returns the current setting of option for alignment of siblings."""
		...

	@overload
	def alignSiblings(self, b : bool) -> None:
		"""Sets the option for alignment of siblings tob."""
		...

	# Module options

	def setSubgraph(self, pSubgraph : AcyclicSubgraphModule) -> None:
		"""Sets the module for the computation of the acyclic subgraph."""
		...

	def __init__(self) -> None:
		"""Creates an instance of longest-path ranking."""
		...
