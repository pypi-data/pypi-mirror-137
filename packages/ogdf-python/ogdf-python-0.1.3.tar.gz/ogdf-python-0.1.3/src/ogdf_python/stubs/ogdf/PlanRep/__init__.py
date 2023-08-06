# file stubs/ogdf/PlanRep/__init__.py generated from classogdf_1_1_plan_rep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanRep(ogdf.GraphCopy):

	"""Planarized representations (of a connected component) of a graph."""

	# Processing connected components

	def numberOfCCs(self) -> int:
		"""Returns the number of connected components in the original graph."""
		...

	def currentCC(self) -> int:
		"""Returns the index of the current connected component (-1 if not yet initialized)."""
		...

	def ccInfo(self) -> CCsInfo:
		"""Returns the connected components info structure."""
		...

	@overload
	def numberOfNodesInCC(self) -> int:
		"""Returns the number of nodes in the current connected component."""
		...

	@overload
	def numberOfNodesInCC(self, cc : int) -> int:
		"""Returns the number of nodes in connected componentcc."""
		...

	def v(self, i : int) -> node:
		"""Returns nodeiin the list of all original nodes."""
		...

	def e(self, i : int) -> edge:
		"""Returns edgeiin the list of all original edges."""
		...

	@overload
	def startNode(self) -> int:
		"""Returns the index of the first node in this connected component."""
		...

	@overload
	def startNode(self, cc : int) -> int:
		"""Returns the index of the first node in connected componentcc."""
		...

	@overload
	def stopNode(self) -> int:
		"""Returns the index of (one past) the last node in this connected component."""
		...

	@overload
	def stopNode(self, cc : int) -> int:
		"""Returns the index of (one past) the last node in connected componentcc."""
		...

	def startEdge(self) -> int:
		"""Returns the index of the first edge in this connected component."""
		...

	def stopEdge(self) -> int:
		"""Returns the index of (one past) the last edge in this connected component."""
		...

	def initCC(self, cc : int) -> None:
		"""Initializes the planarized representation for connected componentcc."""
		...

	# Node expansion

	@overload
	def expandAdj(self, v : node) -> adjEntry:
		"""Returns the adjacency entry of a node of an expanded face."""
		...

	@overload
	def expandAdj(self, v : node) -> adjEntry:
		...

	# Clique boundary

	@overload
	def boundaryAdj(self, v : node) -> adjEntry:
		"""Returns the adjacency entry of the first edge of the inserted boundary at a center node (original) of a clique, 0 if no boundary exists."""
		...

	@overload
	def boundaryAdj(self, v : node) -> adjEntry:
		"""Returns a reference to the adjacency entry of the first edge of the inserted boundary at a center node (original) of a clique, 0 if no boundary exists."""
		...

	def setCliqueBoundary(self, e : edge) -> None:
		...

	def isCliqueBoundary(self, e : edge) -> bool:
		...

	# Node types

	@overload
	def typeOf(self, v : node) -> Graph.NodeType:
		"""Returns the type of nodev."""
		...

	@overload
	def typeOf(self, v : node) -> Graph.NodeType:
		"""Returns a reference to the type of nodev."""
		...

	def isVertex(self, v : node) -> bool:
		"""Returns true if the node represents a "real" object in the original graph."""
		...

	def nodeTypeOf(self, v : node) -> nodeType:
		"""Returns the extended node type ofv."""
		...

	def setCrossingType(self, v : node) -> None:
		"""Classifies nodevas a crossing."""
		...

	def isCrossingType(self, v : node) -> bool:
		"""Returns true iff nodevis classified as a crossing."""
		...

	# Edge types

	@overload
	def typeOf(self, e : edge) -> EdgeType:
		"""Returns the type of edgee."""
		...

	@overload
	def typeOf(self, e : edge) -> EdgeType:
		"""Returns a reference to the type of edgee."""
		...

	def oriEdgeTypes(self, e : edge) -> edgeType:
		"""Returns a reference to the type of original edgee."""
		...

	def edgeTypeOf(self, e : edge) -> edgeType:
		"""Returns the new type field ofe."""
		...

	def edgeTypes(self, e : edge) -> edgeType:
		"""Returns a reference to the new type field ofe."""
		...

	def setEdgeTypeOf(self, e : edge, et : edgeType) -> None:
		"""Sets the new type field of edgeetoet."""
		...

	def setType(self, e : edge, et : EdgeType) -> None:
		"""Set both type values ofeat once."""
		...

	def isGeneralization(self, e : edge) -> bool:
		"""Returns true iff edgeeis classified as generalization."""
		...

	def setGeneralization(self, e : edge) -> None:
		"""Classifies edgeeas generalization (primary type)."""
		...

	def isDependency(self, e : edge) -> bool:
		"""Returns true iff edgeeis classified as dependency."""
		...

	def setDependency(self, e : edge) -> None:
		"""Classifies edgeeas dependency (primary type)."""
		...

	def setAssociation(self, e : edge) -> None:
		"""Classifies edgeeas association (primary type)."""
		...

	def setExpansion(self, e : edge) -> None:
		"""Classifies edgeeas expansion edge (secondary type)."""
		...

	def isExpansion(self, e : edge) -> bool:
		"""Returns true iff edgeeis classified as expansion edge."""
		...

	def isBoundary(self, e : edge) -> bool:
		"""Returns true iff edgeeis a clique boundary."""
		...

	def setAssClass(self, e : edge) -> None:
		"""Classifies edgeeas connection at an association class (tertiary type)."""
		...

	def isAssClass(self, e : edge) -> bool:
		"""Returns true iff edgeeis classified as connection at an association class."""
		...

	def setBrother(self, e : edge) -> None:
		"""Classifies edgeeas connection between hierarchy neighbours (fourth level type)."""
		...

	def setHalfBrother(self, e : edge) -> None:
		"""Classifies edgeeas connection between ... (fourth level type)."""
		...

	def isBrother(self, e : edge) -> bool:
		"""Returns true if edgeeis classified as brother."""
		...

	def isHalfBrother(self, e : edge) -> bool:
		"""Returns true if edgeeis classified as half-brother."""
		...

	def edgeTypeAND(self, e : edge, et : edgeType) -> edgeType:
		"""Sets type of edgeeto current type (bitwise) ANDet."""
		...

	def edgeTypeOR(self, e : edge, et : edgeType) -> edgeType:
		"""Sets type of edgeeto current type (bitwise) ORet."""
		...

	@overload
	def setPrimaryType(self, e : edge, et : edgeType) -> None:
		"""Sets primary edge type of edgeeto primary edge type inet(deletes old primary value)."""
		...

	@overload
	def setPrimaryType(self, e : edge, et : UMLEdgeTypeConstants) -> None:
		"""Sets primary edge type of edgeeto primary edge type inet(deletes old primary value)."""
		...

	def setSecondaryType(self, e : edge, et : edgeType) -> None:
		"""Sets secondary edge type of edgeeto primary edge type inet."""
		...

	def edgeTypePrimaryAND(self, e : edge, et : edgeType) -> edgeType:
		"""Sets primary type ofeto bitwise AND ofet'sprimary value and old value."""
		...

	def edgeTypePrimaryOR(self, e : edge, et : edgeType) -> edgeType:
		"""Sets primary type ofeto bitwise OR ofet'sprimary value and old value."""
		...

	def setUserType(self, e : edge, et : edgeType) -> None:
		"""Sets user defined type locally."""
		...

	def isUserType(self, e : edge, et : edgeType) -> bool:
		"""Returns user defined type."""
		...

	def setExpansionEdge(self, e : edge, expType : int) -> None:
		"""Sets the expansion edge type ofetoexpType."""
		...

	def isExpansionEdge(self, e : edge) -> bool:
		"""Returns ifeis an expansion edge."""
		...

	def expansionType(self, e : edge) -> int:
		"""Returns the expansion edge type ofe."""
		...

	def isDegreeExpansionEdge(self, e : edge) -> bool:
		"""Returns ifeis a degree expansion edge."""
		...

	# Access to attributes in original graph

	@overload
	def widthOrig(self) -> NodeArray[ float ]:
		"""Gives access to the node array of the widths of original nodes."""
		...

	@overload
	def widthOrig(self, v : node) -> float:
		"""Returns the width of original nodev."""
		...

	@overload
	def heightOrig(self) -> NodeArray[ float ]:
		"""Gives access to the node array of the heights of original nodes."""
		...

	@overload
	def heightOrig(self, v : node) -> float:
		"""Returns the height of original nodev."""
		...

	def typeOrig(self, e : edge) -> EdgeType:
		"""Returns the type of original edgee."""
		...

	def getGraphAttributes(self) -> GraphAttributes:
		"""Returns the graph attributes of the original graph (the pointer may be 0)."""
		...

	# Structural alterations

	def expand(self, lowDegreeExpand : bool = False) -> None:
		...

	def expandLowDegreeVertices(self, OR : OrthoRep) -> None:
		...

	@overload
	def collapseVertices(self, OR : OrthoRep, drawing : Layout) -> None:
		...

	@overload
	def collapseVertices(self, OR : OrthoRep, drawing : GridLayout) -> None:
		...

	def removeCrossing(self, v : node) -> None:
		...

	def insertBoundary(self, center : node, adjExternal : adjEntry) -> None:
		...

	# Extension of methods defined by GraphCopys

	def split(self, e : edge) -> edge:
		"""Splits edgee."""
		...

	def expandedNode(self, v : node) -> node:
		...

	def setExpandedNode(self, v : node, w : node) -> None:
		...

	# Creation of new nodes and edges

	@overload
	def newCopy(self, vOrig : node, vType : Graph.NodeType) -> node:
		"""Creates a new node with node typevTypein the planarized representation."""
		...

	@overload
	def newCopy(self, v : node, adjAfter : adjEntry, eOrig : edge) -> edge:
		"""Creates a new edge in the planarized representation."""
		...

	@overload
	def newCopy(self, v : node, adjAfter : adjEntry, eOrig : edge, E : CombinatorialEmbedding) -> edge:
		"""Creates a new edge in the planarized representation while updating the embeddingE."""
		...

	# Crossings

	def insertEdgePath(self, eOrig : edge, crossedEdges : SList[adjEntry]) -> None:
		"""Re-inserts edgeeOrigby "crossing" the edges incrossedEdges."""
		...

	def insertEdgePathEmbedded(self, eOrig : edge, E : CombinatorialEmbedding, crossedEdges : SList[adjEntry]) -> None:
		"""Same as insertEdgePath, but for embedded graphs."""
		...

	def removeEdgePathEmbedded(self, E : CombinatorialEmbedding, eOrig : edge, newFaces : FaceSet[ False ]) -> None:
		"""Removes the complete edge path for edgeeOrigwhile preserving the embedding."""
		...

	def insertCrossing(self, crossingEdge : edge, crossedEdge : edge, topDown : bool) -> edge:
		"""Inserts crossings between two copy edges."""
		...

	# Degree-1 nodes

	#: The index of the current component.
	m_currentCC : int = ...

	m_ccInfo : Graph.CCsInfo = ...

	#: Pointer to graph attributes of original graph.
	m_pGraphAttributes : GraphAttributes = ...

	#: Simple node types.
	m_vType : NodeArray[NodeType] = ...

	#: Node types for extended semantic information.
	m_nodeTypes : NodeArray[nodeType] = ...

	#: For all expansion nodes, save expanded node.
	m_expandedNode : NodeArray[node] = ...

	m_expandAdj : NodeArray[adjEntry] = ...

	m_boundaryAdj : NodeArray[adjEntry] = ...

	m_expansionEdge : EdgeArray[  int ] = ...

	m_eType : EdgeArray[EdgeType] = ...

	m_edgeTypes : EdgeArray[edgeType] = ...

	m_oriEdgeTypes : EdgeArray[edgeType] = ...

	m_eAuxCopy : EdgeArray[edge] = ...

	def removeDeg1Nodes(self, S : ArrayBuffer[Deg1RestoreInfo], mark : NodeArray[ bool ]) -> None:
		"""Removes all marked degree-1 nodes from the graph copy and stores restore information inS."""
		...

	def restoreDeg1Nodes(self, S : ArrayBuffer[Deg1RestoreInfo], deg1s : List[node]) -> None:
		"""Restores degree-1 nodes previously removed withremoveDeg1Nodes()."""
		...

	@overload
	def writeGML(self, fileName : str, OR : OrthoRep, drawing : GridLayout) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream, OR : OrthoRep, drawing : GridLayout) -> None:
		...

	def setCopyType(self, eCopy : edge, eOrig : edge) -> None:
		...

	def generalizationPattern(self) -> edgeType:
		...

	def associationPattern(self) -> edgeType:
		...

	def expansionPattern(self) -> edgeType:
		...

	def assClassPattern(self) -> edgeType:
		...

	def brotherPattern(self) -> edgeType:
		...

	def halfBrotherPattern(self) -> edgeType:
		...

	def cliquePattern(self) -> edgeType:
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a planarized representation of graphG."""
		...

	@overload
	def __init__(self, AG : GraphAttributes) -> None:
		"""Creates a planarized representation of graphAG."""
		...

	def __destruct__(self) -> None:
		...
