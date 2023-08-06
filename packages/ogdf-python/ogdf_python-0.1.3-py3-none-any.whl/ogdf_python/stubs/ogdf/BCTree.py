# file stubs/ogdf/BCTree.py generated from classogdf_1_1_b_c_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BCTree(object):

	"""Static BC-trees."""

	#: The number of B-components.
	m_numB : int = ...

	#: The number of C-components.
	m_numC : int = ...

	m_gNode_isMarked : NodeArray[ bool ] = ...

	#: An injective mapping vertices(G) -> vertices(H).
	m_gNode_hNode : NodeArray[node] = ...

	#: A bijective mapping edges(G) -> edges(H).
	m_gEdge_hEdge : EdgeArray[edge] = ...

	#: Arraythat contains the type of each BC-tree-vertex.
	m_bNode_type : NodeArray[BNodeType] = ...

	#: Arrayof marks for the BC-tree-vertices.
	m_bNode_isMarked : NodeArray[ bool ] = ...

	#: Arraythat contains for each BC-tree-vertex the representantive of its parent within the subgraph in the biconnected components graph belonging to the biconnected component represented by the respective BC-tree-vertex.
	m_bNode_hRefNode : NodeArray[node] = ...

	#: Arraythat contains for each BC-tree-vertex the representant of itself within the subgraph in the biconnected components graph belonging to the biconnected component represented by the parent of the respective BC-tree-vertex.
	m_bNode_hParNode : NodeArray[node] = ...

	#: Arraythat contains for each BC-tree-vertex a linear list of the edges of the biconnected components graph belonging to the biconnected component represented by the respective BC-tree-vertex.
	m_bNode_hEdges : NodeArray[SList[edge] ] = ...

	#: Arraythat contains for each BC-tree-vertex the number of vertices belonging to the biconnected component represented by the respective BC-tree-vertex.
	m_bNode_numNodes : NodeArray[  int ] = ...

	m_hNode_bNode : NodeArray[node] = ...

	#: A surjective mapping edges(H) -> vertices(B).
	m_hEdge_bNode : EdgeArray[node] = ...

	#: A surjective mapping vertices(H) -> vertices(G).
	m_hNode_gNode : NodeArray[node] = ...

	#: A bijective mapping edges(H) -> edges(G).
	m_hEdge_gEdge : EdgeArray[edge] = ...

	m_count : int = ...

	#: Temporary array.
	m_number : NodeArray[  int ] = ...

	#: Temporary array.
	m_lowpt : NodeArray[  int ] = ...

	#: Temporary stack.
	m_eStack : ArrayBuffer[adjEntry] = ...

	#: Temporary array.
	m_gtoh : NodeArray[node] = ...

	#: Temporary list.
	m_nodes : SList[node] = ...

	def parent(self, vB : node) -> node:
		...

	def findNCA(self, uB : node, vB : node) -> node:
		"""Calculates the nearest common ancestor of two vertices of the BC-tree."""
		...

	def typeOfGNode(self, vG : node) -> GNodeType:
		...

	@overload
	def bcproper(self, vG : node) -> node:
		"""Returns a BC-tree-vertex representing a biconnected component which a given vertex of the original graph is belonging to."""
		...

	@overload
	def bcproper(self, eG : edge) -> node:
		"""Returns the BC-tree-vertex representing the biconnected component which a given edge of the original graph is belonging to."""
		...

	@overload
	def rep(self, vG : node) -> node:
		"""Returns a vertex of the biconnected components graph corresponding to a given vertex of the original graph."""
		...

	@overload
	def rep(self, eG : edge) -> edge:
		"""Returns the edge of the biconnected components graph corresponding to a given edge of the original graph."""
		...

	@overload
	def original(self, vH : node) -> node:
		...

	@overload
	def original(self, eH : edge) -> edge:
		"""Returns the edge of the original graph which a given edge of the biconnected components graph is corresponding to."""
		...

	def typeOfBNode(self, vB : node) -> BNodeType:
		...

	def hEdges(self, vB : node) -> SList[edge]:
		"""Returns a linear list of the edges of the biconnected components graph belonging to the biconnected component represented by a given BC-tree-vertex."""
		...

	def numberOfEdges(self, vB : node) -> int:
		"""Returns the number of edges belonging to the biconnected component represented by a given BC-tree-vertex."""
		...

	def numberOfNodes(self, vB : node) -> int:
		"""Returns the number of vertices belonging to the biconnected component represented by a given BC-tree-vertex."""
		...

	def bComponent(self, uG : node, vG : node) -> node:
		...

	def findPath(self, sG : node, tG : node) -> SList[node]:
		"""Calculates a path in the BC-tree."""
		...

	def findPathBCTree(self, sB : node, tB : node) -> SList[node]:
		"""Calculates a path in the BC-tree."""
		...

	def repVertex(self, uG : node, vB : node) -> node:
		"""Returns a vertex of the biconnected components graph corresponding to a given vertex of the original graph and belonging to the representation of a certain biconnected component given by a vertex of the BC-tree."""
		...

	def cutVertex(self, uB : node, vB : node) -> node:
		"""Returns the copy of a cut-vertex in the biconnected components graph which belongs to a certain B-component and leads to another B-component."""
		...

	class BNodeType(enum.Enum):

		"""Enumeration type for characterizing the BC-tree-vertices."""

		#: a vertex representing a B-component
		BComp = enum.auto()

		#: a vertex representing a C-component
		CComp = enum.auto()

	class GNodeType(enum.Enum):

		"""Enumeration type for characterizing the vertices of the original graph."""

		#: an ordinary vertex, i.e. not a cut-vertex
		Normal = enum.auto()

		#: a cut-vertex
		CutVertex = enum.auto()

	#: The BC-tree.
	m_B : Graph = ...

	#: The original graph.
	m_G : Graph = ...

	#: The biconnected components graph.
	m_H : Graph = ...

	def biComp(self, adjuG : adjEntry, vG : node) -> None:
		"""Generates the BC-tree and the biconnected components graph recursively."""
		...

	def init(self, vG : node) -> None:
		"""Initialization."""
		...

	@overload
	def initNotConnected(self, vG : List[node]) -> None:
		"""Initializationfor not connected graphs."""
		...

	@overload
	def initNotConnected(self, vG : node) -> None:
		"""Initializationfor not connected graphs."""
		...

	@overload
	def __init__(self, G : Graph, callInitConnected : bool = False) -> None:
		"""A constructor."""
		...

	@overload
	def __init__(self, G : Graph, vG : List[node]) -> None:
		"""Constructor for not connected graphs."""
		...

	@overload
	def __init__(self, G : Graph, vG : node, callInitConnected : bool = False) -> None:
		"""A constructor."""
		...

	def __destruct__(self) -> None:
		"""Virtual destructor."""
		...

	def auxiliaryGraph(self) -> Graph:
		"""Returns the biconnected components graph."""
		...

	def bcTree(self) -> Graph:
		"""Returns the BC-tree graph."""
		...

	def numberOfBComps(self) -> int:
		"""Returns the number of B-components."""
		...

	def numberOfCComps(self) -> int:
		"""Returns the number of C-components."""
		...

	def originalGraph(self) -> Graph:
		"""Returns the original graph."""
		...
