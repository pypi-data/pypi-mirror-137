# file stubs/ogdf/SPQRTree.py generated from classogdf_1_1_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SPQRTree(object):

	"""Linear-time implementation of static SPQR-trees."""

	# Access operations

	def originalGraph(self) -> Graph:
		"""Returns a reference to the original graphG."""
		...

	def tree(self) -> Graph:
		"""Returns a reference to the treeT."""
		...

	def rootEdge(self) -> edge:
		"""Returns the edge ofGat whichTis rooted."""
		...

	def rootNode(self) -> node:
		"""Returns the root node ofT."""
		...

	def numberOfSNodes(self) -> int:
		"""Returns the number of S-nodes inT."""
		...

	def numberOfPNodes(self) -> int:
		"""Returns the number of P-nodes inT."""
		...

	def numberOfRNodes(self) -> int:
		"""Returns the number of R-nodes inT."""
		...

	def typeOf(self, v : node) -> NodeType:
		"""Returns the type of nodev."""
		...

	def nodesOfType(self, t : NodeType) -> List[node]:
		"""Returns the list of all nodes with typet."""
		...

	def skeleton(self, v : node) -> Skeleton:
		"""Returns the skeleton of nodev."""
		...

	def skeletonOfReal(self, e : edge) -> Skeleton:
		"""Returns the skeleton that contains the real edgee."""
		...

	def copyOfReal(self, e : edge) -> edge:
		"""Returns the skeleton edge that corresponds to the real edgee."""
		...

	def pertinentGraph(self, v : node, Gp : PertinentGraph) -> None:
		"""Returns the pertinent graph of tree nodevinGp."""
		...

	# Update operations

	#: node in pertinent graph corresponding to an original node (auxiliary member)
	m_cpV : NodeArray[node] = ...

	#: list of added nodes (auxiliary member)
	m_cpVAdded : SList[node] = ...

	@overload
	def rootTreeAt(self, e : edge) -> node:
		"""RootsTat edgeeand returns the new root node ofT."""
		...

	@overload
	def rootTreeAt(self, v : node) -> node:
		"""RootsTat nodevand returnsv."""
		...

	def directSkEdge(self, vT : node, e : edge, src : node) -> None:
		...

	def replaceSkEdgeByPeak(self, vT : node, e : edge) -> None:
		...

	def cpRec(self, v : node, Gp : PertinentGraph) -> None:
		"""Recursively performs the task of adding edges (and nodes) to the pertinent graphGpfor each involved skeleton graph."""
		...

	def cpAddEdge(self, eOrig : edge, Gp : PertinentGraph) -> edge:
		"""Add an edge toGpcorresponding toeOrig."""
		...

	def cpAddNode(self, vOrig : node, Gp : PertinentGraph) -> node:
		"""Add a node toGpcorresponding tovOrigif required."""
		...

	class NodeType(enum.Enum):

		"""The type of a tree node in T."""

		SNode = enum.auto()

		PNode = enum.auto()

		RNode = enum.auto()

	def __destruct__(self) -> None:
		...
