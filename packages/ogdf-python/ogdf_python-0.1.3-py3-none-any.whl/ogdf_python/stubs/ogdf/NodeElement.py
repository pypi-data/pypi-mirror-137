# file stubs/ogdf/NodeElement.py generated from classogdf_1_1_node_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ADJLIST = TypeVar('ADJLIST')

EDGELIST = TypeVar('EDGELIST')

class NodeElement(ogdf.internal.GraphElement):

	"""Class for the representation of nodes."""

	#: The container containing all entries in the adjacency list of this node.
	adjEntries : internal.GraphObjectContainer[AdjElement] = ...

	def adjEdges(self, edgeList : EDGELIST) -> None:
		"""Returns a list with all edges incident to this node."""
		...

	def allAdjEntries(self, adjList : ADJLIST) -> None:
		"""Returns a list with all adjacency entries of this node."""
		...

	def degree(self) -> int:
		"""Returns the degree of the node (indegree + outdegree)."""
		...

	def firstAdj(self) -> adjEntry:
		"""Returns the first entry in the adjaceny list."""
		...

	def indeg(self) -> int:
		"""Returns the indegree of the node."""
		...

	def index(self) -> int:
		"""Returns the (unique) node index."""
		...

	def inEdges(self, edgeList : EDGELIST) -> None:
		"""Returns a list with all incoming edges of this node."""
		...

	def lastAdj(self) -> adjEntry:
		"""Returns the last entry in the adjacency list."""
		...

	def outdeg(self) -> int:
		"""Returns the outdegree of the node."""
		...

	def outEdges(self, edgeList : EDGELIST) -> None:
		"""Returns a list with all outgoing edges of this node."""
		...

	def pred(self) -> node:
		"""Returns the predecessor in the list of all nodes."""
		...

	def succ(self) -> node:
		"""Returns the successor in the list of all nodes."""
		...

	def compare(self, x : NodeElement, y : NodeElement) -> int:
		"""Standard Comparer."""
		...
