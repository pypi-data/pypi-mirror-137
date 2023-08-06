# file stubs/ogdf/DynamicSPQRTree.py generated from classogdf_1_1_dynamic_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicSPQRTree(ogdf.SPQRTree, ogdf.DynamicSPQRForest):

	"""Linear-time implementation of dynamic SPQR-trees."""

	#: temporary array used bycreateSkeleton()
	m_mapV : NodeArray[node] = ...

	#: edge ofGat whichTis rooted
	m_rootEdge : edge = ...

	#: pointer to skeleton of a node inT
	m_sk : NodeArray[DynamicSkeleton] = ...

	#: copies of real and virtual edges in their skeleton graphs (invalid, if the skeleton does not actually exist)
	m_skelEdge : EdgeArray[edge] = ...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates an SPQR treeTfor graphGrooted at the first edge ofG."""
		...

	@overload
	def __init__(self, G : Graph, e : edge) -> None:
		"""Creates an SPQR treeTfor graphGrooted at the edgee."""
		...

	def __destruct__(self) -> None:
		...

	def copyOfReal(self, e : edge) -> edge:
		"""Returns the skeleton edge that corresponds to the real edgee."""
		...

	def findPath(self, s : node, t : node) -> SList[node]:
		"""Finds the shortest path between the two sets of vertices ofTwhichsandtofGbelong to."""
		...

	def nodesOfType(self, t : NodeType) -> List[node]:
		"""Returns the list of all nodes with typet."""
		...

	def numberOfPNodes(self) -> int:
		"""Returns the number of P-nodes inT."""
		...

	def numberOfRNodes(self) -> int:
		"""Returns the number of R-nodes inT."""
		...

	def numberOfSNodes(self) -> int:
		"""Returns the number of S-nodes inT."""
		...

	def originalGraph(self) -> Graph:
		"""Returns a reference to the original graphG."""
		...

	def rootEdge(self) -> edge:
		"""Returns the edge ofGat whichTis rooted."""
		...

	def rootNode(self) -> node:
		"""Returns the root node ofT."""
		...

	@overload
	def rootTreeAt(self, e : edge) -> node:
		"""RootsTat edgeeand returns the new root node ofT."""
		...

	@overload
	def rootTreeAt(self, v : node) -> node:
		"""RootsTat nodevand returnsv."""
		...

	def skeleton(self, v : node) -> Skeleton:
		"""Returns the skeleton of nodev."""
		...

	def skeletonEdge(self, v : node, w : node) -> edge:
		"""Returns the virtual edge in the skeleton ofwthat corresponds to the tree edge betweenvandw."""
		...

	def skeletonOfReal(self, e : edge) -> Skeleton:
		"""Returns the skeleton that contains the real edgee."""
		...

	def tree(self) -> Graph:
		"""Returns a reference to the treeT."""
		...

	def typeOf(self, v : node) -> NodeType:
		"""Returns the type of nodev."""
		...

	def updateInsertedEdge(self, e : edge) -> edge:
		"""Updates the whole data structure after a new edgeehas been inserted intoG."""
		...

	def updateInsertedNode(self, e : edge, f : edge) -> node:
		"""Updates the whole data structure after a new vertex has been inserted intoGby splitting an edge intoeandf."""
		...

	def cpRec(self, v : node, Gp : PertinentGraph) -> None:
		"""Recursively performs the task of adding edges (and nodes) to the pertinent graphGpfor each involved skeleton graph."""
		...

	def createSkeleton(self, vT : node) -> DynamicSkeleton:
		"""Creates the skeleton graph belonging to a given vertexvTofT."""
		...

	def init(self, e : edge) -> None:
		"""Initialization(called by constructors)."""
		...
