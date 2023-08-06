# file stubs/ogdf/ShellingOrder.py generated from classogdf_1_1_shelling_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ShellingOrder(object):

	"""The shelling order of a graph."""

	def __init__(self) -> None:
		"""Creates an empty shelling order."""
		...

	def __destruct__(self) -> None:
		...

	def getGraph(self) -> Graph:
		"""Returns the graph associated with the shelling order."""
		...

	def init(self, G : Graph, partition : List[ShellingOrderSet]) -> None:
		"""Initializes the shelling order for graphGwith a given node partition."""
		...

	def initLeftmost(self, G : Graph, partition : List[ShellingOrderSet]) -> None:
		"""Initializes the shelling order for graphGwith a given node partition and transforms it into a leftmost order."""
		...

	def left(self, i : int) -> node:
		"""Returns the left-node of thei-th setVi."""
		...

	def len(self, i : int) -> int:
		"""Returns the length of thei-th order setVi."""
		...

	def length(self) -> int:
		"""Returns the number of sets in the node partition."""
		...

	def __call__(self, i : int, j : int) -> node:
		"""Returns thej-th node of thei-th order setVi."""
		...

	def __getitem__(self, i : int) -> ShellingOrderSet:
		"""Returns thei-th setV_i"""
		...

	def push(self, k : int, v : node, tgt : node) -> None:
		...

	def rank(self, v : node) -> int:
		"""Returns the rank of nodev, where rank(v) =iiffvis contained inVi."""
		...

	def right(self, i : int) -> node:
		"""Returns the right-node of thei-th setVi."""
		...
