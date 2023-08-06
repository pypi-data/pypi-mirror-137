# file stubs/ogdf/EdgeStandardRep.py generated from classogdf_1_1_edge_standard_rep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeStandardRep(ogdf.HypergraphObserver):

	"""Edge standard representation of hypergraphs."""

	@overload
	def __init__(self) -> None:
		"""Creates an edge standard representation."""
		...

	@overload
	def __init__(self, pH : Hypergraph, pType : EdgeStandardType) -> None:
		"""Creates an edge standard rep. of a givenpTypeassociated withpH."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def clear(self) -> None:
		"""Clears all cluster data."""
		...

	def constGraph(self) -> Graph:
		"""Returns a reference to the representation graph."""
		...

	def dummyNodes(self) -> List[node]:
		"""Returns the list of dummy nodes."""
		...

	def edgeMap(self, e : hyperedge) -> List[edge]:
		"""Returns the list of edges associated with the hyperedge."""
		...

	def hyperedgeMap(self, e : edge) -> hyperedge:
		"""Returns the hyperedge associated with the edge."""
		...

	def hypergraph(self) -> Hypergraph:
		"""Conversion to original hypergraph reference."""
		...

	def hypernodeMap(self, v : node) -> hypernode:
		"""Returns the hypernode associated with the node (if any)."""
		...

	def nodeMap(self, v : hypernode) -> node:
		"""Returns the node associated with the hypernode."""
		...

	def type(self) -> EdgeStandardType:
		"""Returns the type of edge standard representation."""
		...

	def cleared(self) -> None:
		"""Hypergraphclean-up reaction."""
		...

	def hyperedgeAdded(self, e : hyperedge) -> None:
		"""Hyperedge addition reaction."""
		...

	def hyperedgeDeleted(self, e : hyperedge) -> None:
		"""Hyperedge removal reaction."""
		...

	def hypernodeAdded(self, v : hypernode) -> None:
		"""Hypernode addition reaction."""
		...

	def hypernodeDeleted(self, v : hypernode) -> None:
		"""Hypernode removal reaction."""
		...
