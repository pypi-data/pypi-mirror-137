# file stubs/ogdf/Graph/HiddenEdgeSet.py generated from classogdf_1_1_graph_1_1_hidden_edge_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HiddenEdgeSet(object):

	"""Functionality for temporarily hiding edges in constant time."""

	def __init__(self, graph : Graph) -> None:
		"""Creates a new set of hidden edges."""
		...

	def __destruct__(self) -> None:
		"""Restores all hidden edges."""
		...

	def hide(self, e : edge) -> None:
		"""Hides the given edge."""
		...

	@overload
	def restore(self) -> None:
		"""Restores all edges contained in this set."""
		...

	@overload
	def restore(self, e : edge) -> None:
		"""Reveals the given edge."""
		...

	def size(self) -> int:
		"""Returns the number of edges contained in this set."""
		...
