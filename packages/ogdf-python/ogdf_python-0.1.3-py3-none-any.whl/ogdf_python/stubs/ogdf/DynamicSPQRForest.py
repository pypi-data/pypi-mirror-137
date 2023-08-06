# file stubs/ogdf/DynamicSPQRForest.py generated from classogdf_1_1_dynamic_s_p_q_r_forest
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicSPQRForest(ogdf.DynamicBCTree):

	"""Dynamic SPQR-forest."""

	m_bNode_SPQR : NodeArray[node] = ...

	#: The numbers of S-components.
	m_bNode_numS : NodeArray[  int ] = ...

	#: The numbers of P-components.
	m_bNode_numP : NodeArray[  int ] = ...

	#: The numbers of R-components.
	m_bNode_numR : NodeArray[  int ] = ...

	#: The types of the SPQR-tree-vertices.
	m_tNode_type : NodeArray[TNodeType] = ...

	#: The owners of the SPQR-tree-vertices in the UNION/FIND structure.
	m_tNode_owner : NodeArray[node] = ...

	#: The virtual edges leading to the parents of the SPQR-tree vertices.
	m_tNode_hRefEdge : NodeArray[edge] = ...

	#: Lists of real and virtual edges belonging to SPQR-tree vertices.
	m_tNode_hEdges : NodeArray[List[edge]  ] = ...

	#: The positions of real and virtual edges in theirm_tNode_hEdgeslists.
	m_hEdge_position : EdgeArray[ListIterator[edge] ] = ...

	#: The SPQR-tree-vertices which the real and virtual edges are belonging to.
	m_hEdge_tNode : EdgeArray[node] = ...

	#: The partners of virtual edges (nullptrif real).
	m_hEdge_twinEdge : EdgeArray[edge] = ...

	#: Auxiliary array used bycreateSPQR().
	m_htogc : NodeArray[node] = ...

	#: Auxiliary array used byfindNCASPQR()
	m_tNode_isMarked : NodeArray[ bool ] = ...

	def uniteSPQR(self, vB : node, sT : node, tT : node) -> node:
		...

	def findSPQR(self, vT : node) -> node:
		"""Finds the proper representative of an SPQR-tree-vertex (FIND part of UNION/FIND)."""
		...

	def findNCASPQR(self, sT : node, tT : node) -> node:
		...

	@overload
	def findPathSPQR(self, sH : node, tH : node, rT : node) -> SList[node]:
		"""Finds the shortest path between the two sets of SPQR-tree-vertices whichsHandtHare belonging to."""
		...

	def updateInsertedEdgeSPQR(self, vB : node, eG : edge) -> edge:
		...

	def updateInsertedNodeSPQR(self, vB : node, eG : edge, fG : edge) -> node:
		"""Updates an SPQR-tree after a new vertex has been inserted into the original graph by splitting an edge intoeGandfG."""
		...

	def spqrproper(self, eH : edge) -> node:
		...

	def twinEdge(self, eH : edge) -> edge:
		"""Returns the twin edge of a given edge ofm_H, if it is virtual, ornullptr, if it is real."""
		...

	def typeOfTNode(self, vT : node) -> TNodeType:
		...

	def hEdgesSPQR(self, vT : node) -> List[edge]:
		"""Returns a linear list of the edges inm_Hbelonging to the triconnected component represented by a given SPQR-tree-vertex."""
		...

	@overload
	def findPathSPQR(self, sH : node, tH : node) -> SList[node]:
		"""Finds the shortest path between the two sets of SPQR-tree-vertices whichsHandtHare belonging to."""
		...

	def virtualEdge(self, vT : node, wT : node) -> edge:
		"""Returns the virtual edge which leads from one vertex of an SPQR-tree to another one."""
		...

	def updateInsertedEdge(self, eG : edge) -> edge:
		...

	def updateInsertedNode(self, eG : edge, fG : edge) -> node:
		"""Updates the whole data structure after a new vertex has been inserted into the original graph by splitting an edge intoeGandfG."""
		...

	class TNodeType(enum.Enum):

		"""Enumeration type for characterizing the SPQR-tree-vertices."""

		#: denotes a vertex representing an S-component
		SComp = enum.auto()

		#: denotes a vertex representing a P-component
		PComp = enum.auto()

		#: denotes a vertex representing an R-component
		RComp = enum.auto()

	#: AGraphstructure containing all SPQR-trees.
	m_T : Graph = ...

	def addHEdge(self, eH : edge, vT : node) -> None:
		"""Adds edgeeHto a vertexvTof the SPQRForest."""
		...

	def createSPQR(self, vB : node) -> None:
		"""Creates the SPQR-tree for a given B-component of the BC-tree."""
		...

	def delHEdge(self, eH : edge, vT : node) -> None:
		"""Deletes edgeeHfromm_Hand removes its connection to a vertexvTof the SPQRForest."""
		...

	def init(self) -> None:
		"""Initialization."""
		...

	def newSPQRNode(self, vB : node, spqrNodeType : TNodeType) -> node:
		"""Creates a new node in the SPQR-tree for a given B-component of the BC-tree."""
		...

	def newTwinEdge(self, eH : edge, vT : node) -> edge:
		"""Creates a twin edge foreH, adds it tovTand returns it."""
		...

	def __init__(self, G : Graph) -> None:
		"""A constructor."""
		...

	def __destruct__(self) -> None:
		...
