# file stubs/ogdf/EdgeElement.py generated from classogdf_1_1_edge_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeElement(ogdf.internal.GraphElement):

	"""Class for the representation of edges."""

	def adjSource(self) -> adjEntry:
		"""Returns the corresponding adjacancy entry at source node."""
		...

	def adjTarget(self) -> adjEntry:
		"""Returns the corresponding adjacancy entry at target node."""
		...

	def commonNode(self, e : edge) -> node:
		"""Returns the common node of the edge ande. Returns nullptr if the two edges are not adjacent."""
		...

	def getAdj(self, v : node) -> adjEntry:
		"""Returns an adjacency entry of this edge at nodev. If this is a self-loop the source adjacency entry will always be returned."""
		...

	def index(self) -> int:
		"""Returns the index of the edge."""
		...

	def isAdjacent(self, e : edge) -> bool:
		"""Returns true iffeis adjacent to the edge."""
		...

	def isIncident(self, v : node) -> bool:
		"""Returns true iffvis incident to the edge."""
		...

	def isInvertedDirected(self, e : edge) -> bool:
		"""Returns true iff edgeeis an inverted edge to this (directed) edge."""
		...

	def isParallelDirected(self, e : edge) -> bool:
		"""Returns true iff edgeeis parallel to this (directed) edge (or if it is the same edge)"""
		...

	def isParallelUndirected(self, e : edge) -> bool:
		"""Returns true iff edgeeis parallel to this (undirected) edge (or if it is the same edge)"""
		...

	def isSelfLoop(self) -> bool:
		"""Returns true iff the edge is a self-loop (source node = target node)."""
		...

	def nodes(self) -> std.array[node, 2 ]:
		"""Returns a list of adjacent nodes. If this edge is a self-loop, both entries will be the same node."""
		...

	def opposite(self, v : node) -> node:
		"""Returns the adjacent node different fromv."""
		...

	def pred(self) -> edge:
		"""Returns the predecessor in the list of all edges."""
		...

	def source(self) -> node:
		"""Returns the source node of the edge."""
		...

	def succ(self) -> edge:
		"""Returns the successor in the list of all edges."""
		...

	def target(self) -> node:
		"""Returns the target node of the edge."""
		...

	def compare(self, x : EdgeElement, y : EdgeElement) -> int:
		"""Standard Comparer."""
		...
