# file stubs/ogdf/GraphCopySimple.py generated from classogdf_1_1_graph_copy_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphCopySimple(ogdf.Graph):

	"""Copies of graphs with mapping between nodes and edges."""

	@overload
	def __init__(self) -> None:
		"""Constructs aGraphCopySimpleassociated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs a copy of graphG."""
		...

	@overload
	def __init__(self, GC : GraphCopySimple) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def copy(self, adj : adjEntry) -> adjEntry:
		"""Returns the adjacency entry in the graph copy corresponding toadj."""
		...

	@overload
	def copy(self, e : edge) -> edge:
		"""Returns the edge in the graph copy corresponding toe."""
		...

	@overload
	def copy(self, v : node) -> node:
		"""Returns the node in the graph copy corresponding tov."""
		...

	def createEmpty(self, G : Graph) -> None:
		"""Re-initializes the copy usingG, but does not create any nodes or edges."""
		...

	def delEdge(self, e : edge) -> None:
		"""Removes edgee."""
		...

	def delNode(self, v : node) -> None:
		"""Removes nodev."""
		...

	def init(self, G : Graph) -> None:
		"""Re-initializes the copy usingG."""
		...

	@overload
	def isDummy(self, e : edge) -> bool:
		"""Returns true iffehas no corresponding edge in the original graph."""
		...

	@overload
	def isDummy(self, v : node) -> bool:
		"""Returns true iffvhas no corresponding node in the original graph."""
		...

	@overload
	def newEdge(self, adjSrc : adjEntry, adjTgt : adjEntry, dir : Direction = Direction.after) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	@overload
	def newEdge(self, adjSrc : adjEntry, w : node) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	@overload
	def newEdge(self, eOrig : edge) -> edge:
		"""Creates a new edge in the graph copy with original edgeeOrig."""
		...

	@overload
	def newEdge(self, v : node, adjTgt : adjEntry) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	@overload
	def newEdge(self, v : node, w : node) -> edge:
		"""Creates a new edge (v,w) and returns it."""
		...

	@overload
	def newEdge(self, v : node, w : node, index : int) -> edge:
		"""Creates a new edge (v,w) with predefined index and returns it."""
		...

	@overload
	def newNode(self) -> node:
		"""Creates a new node and returns it."""
		...

	@overload
	def newNode(self, index : int) -> node:
		"""Creates a new node with predefined index and returns it."""
		...

	@overload
	def newNode(self, vOrig : node) -> node:
		"""Creates a new node in the graph copy with original nodevOrig."""
		...

	def __assign__(self, GC : GraphCopySimple) -> GraphCopySimple:
		"""Assignment operator."""
		...

	@overload
	def original(self) -> Graph:
		"""Returns a reference to the original graph."""
		...

	@overload
	def original(self, adj : adjEntry) -> adjEntry:
		"""Returns the adjacency entry in the original graph corresponding toadj."""
		...

	@overload
	def original(self, e : edge) -> edge:
		"""Returns the edge in the original graph corresponding toe."""
		...

	@overload
	def original(self, v : node) -> node:
		"""Returns the node in the original graph corresponding tov."""
		...
