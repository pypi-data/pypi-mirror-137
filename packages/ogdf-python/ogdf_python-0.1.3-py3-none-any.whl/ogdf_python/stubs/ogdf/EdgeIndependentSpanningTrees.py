# file stubs/ogdf/EdgeIndependentSpanningTrees.py generated from classogdf_1_1_edge_independent_spanning_trees
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeIndependentSpanningTrees(object):

	"""Calculates k edge-independent spanning trees of a graph."""

	#: The solution type.
	Solution : Type = EdgeArray[ std.pair[   int,   int ] ]

	@overload
	def __init__(self) -> None:
		"""Creates an instance of edge-independent spanning tree withou associated graph and root."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates an instance of edge-independent spanning tree and sets the graph."""
		...

	@overload
	def __init__(self, G : Graph, root : node) -> None:
		"""Creates an instance of edge-independent spanning tree and sets the graph and root node."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def findAll(self, k : int) -> List[Solution]:
		"""Finds all k edge-independent spanning trees in graphm_Grooted atm_root."""
		...

	def findAllPerm(self, k : int) -> List[Solution]:
		"""Finds all k edge-independent spanning trees in graphm_Grooted atm_root, including permutations."""
		...

	def findOne(self, k : int, f : Solution) -> bool:
		"""Finds k edge-independent spanning trees in graphm_Grooted atm_root."""
		...

	def getGraph(self) -> Graph:
		"""Returns a pointer to the associated graph."""
		...

	def getRoot(self) -> node:
		"""Returns the associated root node."""
		...

	def setGraph(self, G : Graph) -> None:
		"""Sets the associated graph."""
		...

	def setRoot(self, root : node) -> None:
		"""Sets the associated root node."""
		...

	def findDo(self, k : int, func : Callable) -> None:
		"""Finds k edge-independent spanning trees and invokesfuncfor each one, The search is stopped iffuncreturns false."""
		...
