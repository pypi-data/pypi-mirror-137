# file stubs/ogdf/AdjHypergraphElement.py generated from classogdf_1_1_adj_hypergraph_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AdjHypergraphElement(ogdf.internal.GraphElement):

	"""Class for adjacency list elements."""

	OGDF_NEW_DELETE = ...

	def cyclicPred(self) -> adjHypergraphEntry:
		"""Returns the cyclic predecessor in the adjacency list."""
		...

	def cyclicSucc(self) -> adjHypergraphEntry:
		"""Returns the cyclic successor in the adjacency list."""
		...

	def element(self) -> GraphElement:
		"""Returns the element associated with this adjacency entry."""
		...

	def index(self) -> int:
		"""Returns the index of this adjacency element."""
		...

	def pred(self) -> adjHypergraphEntry:
		"""Returns the predecessor in the adjacency list."""
		...

	def succ(self) -> adjHypergraphEntry:
		"""Returns the successor in the adjacency list."""
		...

	def twin(self) -> adjHypergraphEntry:
		"""Returns the pointer to a twin adjacency list."""
		...
