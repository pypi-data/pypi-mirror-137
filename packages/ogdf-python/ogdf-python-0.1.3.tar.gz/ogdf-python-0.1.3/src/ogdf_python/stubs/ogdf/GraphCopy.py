# file stubs/ogdf/GraphCopy.py generated from classogdf_1_1_graph_copy
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphCopy(ogdf.Graph):

	"""Copies of graphs supporting edge splitting."""

	# Mapping between original graph and copy

	@overload
	def original(self) -> Graph:
		"""Returns a reference to the original graph."""
		...

	@overload
	def original(self, v : node) -> node:
		"""Returns the node in the original graph corresponding tov."""
		...

	@overload
	def original(self, e : edge) -> edge:
		"""Returns the edge in the original graph corresponding toe."""
		...

	@overload
	def original(self, adj : adjEntry) -> adjEntry:
		"""Returns the adjacency entry in the original graph corresponding toadj."""
		...

	@overload
	def copy(self, v : node) -> node:
		"""Returns the node in the graph copy corresponding tov."""
		...

	def chain(self, e : edge) -> List[edge]:
		"""Returns the list of edges coresponding to edgee."""
		...

	@overload
	def copy(self, e : edge) -> edge:
		"""Returns the first edge in the list of edges coresponding to edgee."""
		...

	@overload
	def copy(self, adj : adjEntry) -> adjEntry:
		"""Returns the adjacency entry in the copy graph corresponding toadj."""
		...

	@overload
	def isDummy(self, v : node) -> bool:
		"""Returns true iffvhas no corresponding node in the original graph."""
		...

	@overload
	def isDummy(self, e : edge) -> bool:
		"""Returns true iffehas no corresponding edge in the original graph."""
		...

	def isReversed(self, e : edge) -> bool:
		"""Returns true iff edgeehas been reversed."""
		...

	def isReversedCopyEdge(self, e : edge) -> bool:
		"""Returns true iffeis reversed w.r.t."""
		...

	# Creation and deletion of nodes and edges

	@overload
	def newNode(self, vOrig : node) -> node:
		"""Creates a new node in the graph copy with original nodevOrig."""
		...

	def delNode(self, v : node) -> None:
		"""Removes nodevand all its adjacent edges cleaning-up their corresponding lists of original edges."""
		...

	def delEdge(self, e : edge) -> None:
		"""Removes edge e and clears the list of edges corresponding toe'soriginal edge."""
		...

	def clear(self) -> None:
		"""Removes all nodes and all edges from the graph."""
		...

	def split(self, e : edge) -> edge:
		"""Splits edgee."""
		...

	def unsplit(self, eIn : edge, eOut : edge) -> None:
		"""Undoes a previous split operation."""
		...

	@overload
	def newEdge(self, eOrig : edge) -> edge:
		"""Creates a new edge (v,w) with original edgeeOrig."""
		...

	def setEdge(self, eOrig : edge, eCopy : edge) -> None:
		"""sets eOrig to be the corresponding original edge of eCopy and vice versa"""
		...

	def embed(self) -> bool:
		"""Embeds the graph copy."""
		...

	def removePseudoCrossings(self) -> None:
		"""Removes all crossing nodes which are actually only two "touching" edges."""
		...

	@overload
	def insertEdgePath(self, eOrig : edge, crossedEdges : SList[adjEntry]) -> None:
		"""Re-inserts edgeeOrigby "crossing" the edges incrossedEdges."""
		...

	@overload
	def insertEdgePath(self, srcOrig : node, tgtOrig : node, crossedEdges : SList[adjEntry]) -> None:
		"""Special version (forFixedEmbeddingUpwardEdgeInserteronly)."""
		...

	def removeEdgePath(self, eOrig : edge) -> None:
		"""Removes the complete edge path for edgeeOrig."""
		...

	def insertCrossing(self, crossingEdge : edge, crossedEdge : edge, rightToLeft : bool) -> edge:
		"""Inserts crossings between two copy edges."""
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

	# Combinatorial Embeddings

	@overload
	def newEdge(self, v : node, adj : adjEntry, eOrig : edge, E : CombinatorialEmbedding) -> edge:
		"""Creates a new edge with original edgeeOrigin an embeddingE."""
		...

	def setOriginalEmbedding(self) -> None:
		"""Sets the embedding of the graph copy to the embedding of the original graph."""
		...

	def insertEdgePathEmbedded(self, eOrig : edge, E : CombinatorialEmbedding, crossedEdges : SList[adjEntry]) -> None:
		"""Re-inserts edgeeOrigby "crossing" the edges incrossedEdgesin embeddingE."""
		...

	def removeEdgePathEmbedded(self, E : CombinatorialEmbedding, eOrig : edge, newFaces : FaceSet[ False ]) -> None:
		"""Removes the complete edge path for edgeeOrigwhile preserving the embedding."""
		...

	# Miscellaneous

	def init(self, G : Graph) -> None:
		"""Re-initializes the copy using the graphG."""
		...

	def createEmpty(self, G : Graph) -> None:
		"""Associates the graph copy withG, but does not create any nodes or edges."""
		...

	def initByCC(self, info : CCsInfo, cc : int, eCopy : EdgeArray[edge]) -> None:
		"""Initializes the graph copy for the nodes in componentcc."""
		...

	def initByNodes(self, origNodes : List[node], eCopy : EdgeArray[edge]) -> None:
		"""Initializes the graph copy for the nodes in a component."""
		...

	def initByActiveNodes(self, nodeList : List[node], activeNodes : NodeArray[ bool ], eCopy : EdgeArray[edge]) -> None:
		"""Initializes the graph copy for the nodes innodeList."""
		...

	# Operators

	def __assign__(self, GC : GraphCopy) -> GraphCopy:
		"""Assignment operator."""
		...

	def removeUnnecessaryCrossing(self, adjA1 : adjEntry, adjA2 : adjEntry, adjB1 : adjEntry, adjB2 : adjEntry) -> None:
		...

	#: The corresponding list of edges in the graph copy.
	m_eCopy : EdgeArray[List[edge] ] = ...

	#: The position of copy edge in the list.
	m_eIterator : EdgeArray[ListIterator[edge] ] = ...

	#: The corresponding edge in the original graph.
	m_eOrig : EdgeArray[edge] = ...

	#: The original graph.
	m_pGraph : Graph = ...

	#: The corresponding node in the graph copy.
	m_vCopy : NodeArray[node] = ...

	#: The corresponding node in the original graph.
	m_vOrig : NodeArray[node] = ...

	@overload
	def __init__(self) -> None:
		"""Default constructor (does nothing!)."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a graph copy ofG."""
		...

	@overload
	def __init__(self, GC : GraphCopy) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...
