# file stubs/ogdf/Graph/__init__.py generated from classogdf_1_1_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ArrayBase = TypeVar('ArrayBase')

CONTAINER = TypeVar('CONTAINER')

ADJ_ENTRY_LIST = TypeVar('ADJ_ENTRY_LIST')

NODELIST = TypeVar('NODELIST')

class Graph(object):

	"""Data type for general directed graphs (adjacency list representation)."""

	# Iterators

	#: Provides a bidirectional iterator to a node in a graph.
	node_iterator : Type = internal.GraphIterator[node]

	#: Provides a bidirectional iterator to an edge in a graph.
	edge_iterator : Type = internal.GraphIterator[edge]

	#: Provides a bidirectional iterator to an entry in an adjacency list.
	adjEntry_iterator : Type = internal.GraphIterator[adjEntry]

	# Enumerations

	class EdgeType(enum.Enum):

		"""The type of edges (only used in derived classes)."""

		association = enum.auto()

		generalization = enum.auto()

		dependency = enum.auto()

	class NodeType(enum.Enum):

		"""The type of nodes."""

		vertex = enum.auto()

		dummy = enum.auto()

		generalizationMerger = enum.auto()

		generalizationExpander = enum.auto()

		highDegreeExpander = enum.auto()

		lowDegreeExpander = enum.auto()

		associationClass = enum.auto()

	# Graph object containers

	#: The container containing all node objects.
	nodes : internal.GraphObjectContainer[NodeElement] = ...

	#: The container containing all edge objects.
	edges : internal.GraphObjectContainer[EdgeElement] = ...

	@overload
	def __init__(self) -> None:
		"""Constructs an empty graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs a graph that is a copy ofG."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	# Access methods

	def empty(self) -> bool:
		"""Returns true iff the graph is empty, i.e., contains no nodes."""
		...

	def numberOfNodes(self) -> int:
		"""Returns the number of nodes in the graph."""
		...

	def numberOfEdges(self) -> int:
		"""Returns the number of edges in the graph."""
		...

	def maxNodeIndex(self) -> int:
		"""Returns the largest used node index."""
		...

	def maxEdgeIndex(self) -> int:
		"""Returns the largest used edge index."""
		...

	def maxAdjEntryIndex(self) -> int:
		"""Returns the largest used adjEntry index."""
		...

	def nodeArrayTableSize(self) -> int:
		"""Returns the table size of node arrays associated with this graph."""
		...

	def edgeArrayTableSize(self) -> int:
		"""Returns the table size of edge arrays associated with this graph."""
		...

	def adjEntryArrayTableSize(self) -> int:
		"""Returns the table size of adjEntry arrays associated with this graph."""
		...

	def firstNode(self) -> node:
		"""Returns the first node in the list of all nodes."""
		...

	def lastNode(self) -> node:
		"""Returns the last node in the list of all nodes."""
		...

	def firstEdge(self) -> edge:
		"""Returns the first edge in the list of all edges."""
		...

	def lastEdge(self) -> edge:
		"""Returns the last edge in the list of all edges."""
		...

	def chooseNode(self, includeNode : Callable = print, isFastTest : bool = True) -> node:
		"""Returns a random node."""
		...

	def chooseEdge(self, includeEdge : Callable = print, isFastTest : bool = True) -> edge:
		"""Returns a random edge."""
		...

	def allNodes(self, nodeContainer : CONTAINER) -> None:
		"""Returns a container with all nodes of the graph."""
		...

	def allEdges(self, edgeContainer : CONTAINER) -> None:
		"""Returns a container with all edges of the graph."""
		...

	# Creation of new nodes and edges

	@overload
	def newNode(self) -> node:
		"""Creates a new node and returns it."""
		...

	@overload
	def newNode(self, index : int) -> node:
		"""Creates a new node with predefined index and returns it."""
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
	def newEdge(self, adjSrc : adjEntry, adjTgt : adjEntry, dir : Direction = Direction.after) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	@overload
	def newEdge(self, v : node, adjTgt : adjEntry) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	@overload
	def newEdge(self, adjSrc : adjEntry, w : node) -> edge:
		"""Creates a new edge at predefined positions in the adjacency lists."""
		...

	# Removing nodes and edges

	def delNode(self, v : node) -> None:
		"""Removes nodevand all incident edges from the graph."""
		...

	def delEdge(self, e : edge) -> None:
		"""Removes edgeefrom the graph."""
		...

	def clear(self) -> None:
		"""Removes all nodes and all edges from the graph."""
		...

	# Advanced modification methods

	@overload
	def insert(self, G : Graph, nodeMap : NodeArray[node]) -> None:
		"""InsertsGraphGas a subgraph into thisGraph."""
		...

	@overload
	def insert(self, G : Graph) -> None:
		"""InsertsGraphGas a subgraph into thisGraph."""
		...

	def split(self, e : edge) -> edge:
		"""Splits edgeeinto two edges introducing a new node."""
		...

	@overload
	def unsplit(self, u : node) -> None:
		"""Undoes a split operation."""
		...

	@overload
	def unsplit(self, eIn : edge, eOut : edge) -> None:
		"""Undoes a split operation."""
		...

	def splitNode(self, adjStartLeft : adjEntry, adjStartRight : adjEntry) -> node:
		"""Splits a node while preserving the order of adjacency entries."""
		...

	def contract(self, e : edge) -> node:
		"""Contracts edgeewhile preserving the order of adjacency entries."""
		...

	def move(self, e : edge, adjSrc : adjEntry, dirSrc : Direction, adjTgt : adjEntry, dirTgt : Direction) -> None:
		"""Moves edgeeto a different adjacency list."""
		...

	@overload
	def moveTarget(self, e : edge, w : node) -> None:
		"""Moves the target node of edgeeto nodew."""
		...

	@overload
	def moveTarget(self, e : edge, adjTgt : adjEntry, dir : Direction) -> None:
		"""Moves the target node of edgeeto a specific position in an adjacency list."""
		...

	@overload
	def moveSource(self, e : edge, w : node) -> None:
		"""Moves the source node of edgeeto nodew."""
		...

	@overload
	def moveSource(self, e : edge, adjSrc : adjEntry, dir : Direction) -> None:
		"""Moves the source node of edgeeto a specific position in an adjacency list."""
		...

	def searchEdge(self, v : node, w : node, directed : bool = False) -> edge:
		"""Searches and returns an edge connecting nodesvandwin timeO( min(deg(v), deg(w)))."""
		...

	def reverseEdge(self, e : edge) -> None:
		"""Reverses the edgee, i.e., exchanges source and target node."""
		...

	def reverseAllEdges(self) -> None:
		"""Reverses all edges in the graph."""
		...

	def collapse(self, nodesToCollapse : NODELIST) -> None:
		"""Collapses all nodes in the listnodesToCollapseto the first node in the list."""
		...

	def sort(self, v : node, newOrder : ADJ_ENTRY_LIST) -> None:
		"""Sorts the adjacency list of nodevaccording tonewOrder."""
		...

	@overload
	def reverseAdjEdges(self, v : node) -> None:
		"""Reverses the adjacency list ofv."""
		...

	def moveAdj(self, adjMove : adjEntry, dir : Direction, adjPos : adjEntry) -> None:
		"""Moves adjacency entryadjMovebefore or afteradjPos."""
		...

	def moveAdjAfter(self, adjMove : adjEntry, adjAfter : adjEntry) -> None:
		"""Moves adjacency entryadjMoveafteradjAfter."""
		...

	def moveAdjBefore(self, adjMove : adjEntry, adjBefore : adjEntry) -> None:
		"""Moves adjacency entryadjMovebeforeadjBefore."""
		...

	@overload
	def reverseAdjEdges(self) -> None:
		"""Reverses all adjacency lists."""
		...

	def swapAdjEdges(self, adj1 : adjEntry, adj2 : adjEntry) -> None:
		"""Exchanges two entries in an adjacency list."""
		...

	# Miscellaneous

	def genus(self) -> int:
		"""Returns the genus of the graph's embedding."""
		...

	def representsCombEmbedding(self) -> bool:
		"""Returns true iff the graph represents a combinatorial embedding."""
		...

	# Registering arrays and observers

	@overload
	def registerArray(self, pNodeArray : NodeArrayBase) -> ListIterator[NodeArrayBase]:
		"""Registers a node array."""
		...

	@overload
	def registerArray(self, pEdgeArray : EdgeArrayBase) -> ListIterator[EdgeArrayBase]:
		"""Registers an edge array."""
		...

	@overload
	def registerArray(self, pAdjArray : AdjEntryArrayBase) -> ListIterator[AdjEntryArrayBase]:
		"""Registers an adjEntry array."""
		...

	def registerStructure(self, pStructure : GraphObserver) -> ListIterator[GraphObserver]:
		"""Registers a graph observer (e.g. aClusterGraph)."""
		...

	@overload
	def unregisterArray(self, it : ListIterator[NodeArrayBase]) -> None:
		"""Unregisters a node array."""
		...

	@overload
	def unregisterArray(self, it : ListIterator[EdgeArrayBase]) -> None:
		"""Unregisters an edge array."""
		...

	@overload
	def unregisterArray(self, it : ListIterator[AdjEntryArrayBase]) -> None:
		"""Unregisters an adjEntry array."""
		...

	def unregisterStructure(self, it : ListIterator[GraphObserver]) -> None:
		"""Unregisters a graph observer."""
		...

	def moveRegisterArray(self, it : ListIterator[ ArrayBase  ], pArray : ArrayBase) -> None:
		"""Move the registrationitof an graph element array topArray(used with move semantics for graph element arrays)."""
		...

	def resetEdgeIdCount(self, maxId : int) -> None:
		"""Resets the edge id count tomaxId."""
		...

	# Operators

	def __assign__(self, G : Graph) -> Graph:
		"""Assignment operator."""
		...

	def construct(self, G : Graph, mapNode : NodeArray[node], mapEdge : EdgeArray[edge]) -> None:
		...

	def assign(self, G : Graph, mapNode : NodeArray[node], mapEdge : EdgeArray[edge]) -> None:
		...

	def constructInitByNodes(self, G : Graph, nodeList : List[node], mapNode : NodeArray[node], mapEdge : EdgeArray[edge]) -> None:
		"""Constructs a copy of the subgraph ofGinduced bynodeList."""
		...

	def constructInitByActiveNodes(self, nodeList : List[node], activeNodes : NodeArray[ bool ], mapNode : NodeArray[node], mapEdge : EdgeArray[edge]) -> None:
		...

	def constructInitByCC(self, info : CCsInfo, cc : int, mapNode : NodeArray[node], mapEdge : EdgeArray[edge]) -> None:
		"""Constructs a copy of connected componentccininfo."""
		...
