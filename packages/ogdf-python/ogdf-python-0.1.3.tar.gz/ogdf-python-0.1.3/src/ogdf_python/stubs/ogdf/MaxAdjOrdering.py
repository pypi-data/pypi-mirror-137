# file stubs/ogdf/MaxAdjOrdering.py generated from classogdf_1_1_max_adj_ordering
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MaxAdjOrdering(object):

	"""Calculate one or all Maximum Adjacency Ordering(s) of a given simple undirected graph."""

	def __init__(self) -> None:
		"""Standard constructor."""
		...

	def __destruct__(self) -> None:
		"""Standard destructor."""
		...

	@overload
	def calc(self, G : Graph, MAO : ListPure[node]) -> None:
		"""Calculates one MAO starting with the node with index 0."""
		...

	@overload
	def calc(self, G : Graph, MAO : ListPure[node], Forests : ListPure[ListPure[edge]]) -> None:
		"""Calculates one MAO starting with the node with index 0."""
		...

	@overload
	def calc(self, G : Graph, s : node, MAO : ListPure[node]) -> None:
		"""Calculates one MAO starting with a given node."""
		...

	@overload
	def calc(self, G : Graph, s : node, MAO : ListPure[node], Forests : ListPure[ListPure[edge]]) -> None:
		"""Calculates one MAO starting with a given node."""
		...

	@overload
	def calcAll(self, G : Graph, MAOs : ListPure[ListPure[node]]) -> None:
		"""Calculates all MAOs of a given graph."""
		...

	@overload
	def calcAll(self, G : Graph, MAOs : ListPure[ListPure[node]], Fs : ListPure[ListPure[ListPure[edge]]]) -> None:
		"""Calculates all MAOs including their associated forest decompositions of a given graph."""
		...

	def calcBfs(self, G : Graph, MAO : ListPure[node]) -> None:
		"""Calculates one MAO starting with the node with index 0 and lex-bfs tie breaking."""
		...

	def testIfAllMAOs(self, G : Graph, Orderings : ListPure[ListPure[node]], Perms : ListPure[ListPure[node]]) -> bool:
		"""testIfAllMAOs checks all permutations (must be provided) if they are a MAO and if yes searches this ordering in the provided list."""
		...

	def testIfMAO(self, G : Graph, Ordering : ListPure[node]) -> bool:
		"""Test if a given ordering is a MAO."""
		...

	def testIfMAOBfs(self, G : Graph, Ordering : ListPure[node]) -> bool:
		"""Test if a given ordering is a MAO that follows lex-bfs tie breaking."""
		...

	@overload
	def visualize(self, GA : GraphAttributes, MAO : ListPure[node]) -> None:
		"""Convenient way to visualize a MAO with theLinearLayoutclass."""
		...

	@overload
	def visualize(self, GA : GraphAttributes, MAO : ListPure[node], F : ListPure[ListPure[edge]]) -> None:
		"""Convenient way to visualize a MAO with theLinearLayoutclass."""
		...
