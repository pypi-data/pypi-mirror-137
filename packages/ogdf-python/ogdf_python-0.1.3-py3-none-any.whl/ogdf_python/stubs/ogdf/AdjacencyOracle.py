# file stubs/ogdf/AdjacencyOracle.py generated from classogdf_1_1_adjacency_oracle
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AdjacencyOracle(object):

	"""Tells you in constant time if two nodes are adjacent."""

	def __init__(self, G : Graph, degreeThreshold : int = 32) -> None:
		"""The constructor for the class, needs time O(n^2 + m) ∩ Ω(n)."""
		...

	def __destruct__(self) -> None:
		"""The destructor."""
		...

	def adjacent(self, v : node, w : node) -> bool:
		"""Returns true iff verticesvandware adjacent."""
		...
