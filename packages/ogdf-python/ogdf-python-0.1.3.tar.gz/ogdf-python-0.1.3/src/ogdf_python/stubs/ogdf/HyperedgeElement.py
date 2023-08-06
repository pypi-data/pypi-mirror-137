# file stubs/ogdf/HyperedgeElement.py generated from classogdf_1_1_hyperedge_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
NODELIST = TypeVar('NODELIST')

class HyperedgeElement(ogdf.internal.GraphElement):

	"""Class for the representation of hyperedges."""

	OGDF_NEW_DELETE = ...

	def allHypernodes(self, hypernodes : NODELIST) -> None:
		"""Returns a list with all incident hypernodes of the hyperedge."""
		...

	def cardinality(self) -> int:
		"""Returns the number of incident hypernodes."""
		...

	def firstAdj(self) -> adjHypergraphEntry:
		"""Returns the first entry in the adjaceny list."""
		...

	def hypergraph(self) -> Hypergraph:
		"""Returns the hypergraph containing the hyperedge."""
		...

	def incident(self, v : hypernode) -> bool:
		"""Returns true iffvis incident to the hyperedge."""
		...

	def incidentHypernodes(self) -> internal.GraphList[AdjHypergraphElement]:
		"""Returns the incident hypernodes of the hyperedge."""
		...

	def index(self) -> int:
		"""Returns the index of a hyperedge."""
		...

	def lastAdj(self) -> adjHypergraphEntry:
		"""Returns the last entry in the adjacency list."""
		...

	def __eq__(self, e : hyperedge) -> bool:
		"""Equality operator."""
		...

	def pred(self) -> hyperedge:
		"""Returns the predecessor in the list of all hyperedges."""
		...

	def succ(self) -> hyperedge:
		"""Returns the successor in the list of all hyperedges."""
		...
