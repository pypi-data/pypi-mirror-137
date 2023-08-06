# file stubs/ogdf/StaticSPQRTree.py generated from classogdf_1_1_static_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StaticSPQRTree(ogdf.SPQRTree):

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

	def skeletonEdgeSrc(self, e : edge) -> edge:
		"""Returns the edge in skeleton of source(e) that corresponds to tree edgee."""
		...

	def skeletonEdgeTgt(self, e : edge) -> edge:
		"""Returns the edge in skeleton of target(e) that corresponds to tree edgee."""
		...

	def skeletonOfReal(self, e : edge) -> Skeleton:
		"""Returns the skeleton that contains the real edgee."""
		...

	def copyOfReal(self, e : edge) -> edge:
		"""Returns the skeleton edge that corresponds to the real edgee."""
		...

	# Update operations

	@overload
	def rootTreeAt(self, e : edge) -> node:
		"""RootsTat edgeeand returns the new root node ofT."""
		...

	@overload
	def rootTreeAt(self, v : node) -> node:
		"""RootsTat nodevand returnsv."""
		...

	#: skeleton edge corresponding to real edgee
	m_copyOf : EdgeArray[edge] = ...

	#: number of P-nodes
	m_numP : int = ...

	#: number of R-nodes
	m_numR : int = ...

	#: number of S-nodes
	m_numS : int = ...

	#: pointer to original graph
	m_pGraph : Graph = ...

	#: edge ofGat whichTis rooted
	m_rootEdge : edge = ...

	#: root node ofT
	m_rootNode : node = ...

	#: pointer to skeleton of a node inT
	m_sk : NodeArray[StaticSkeleton] = ...

	#: corresponding edge in skeleton(source(e))
	m_skEdgeSrc : EdgeArray[edge] = ...

	#: corresponding edge in skeleton(target(e))
	m_skEdgeTgt : EdgeArray[edge] = ...

	#: skeleton containing real edgee
	m_skOf : EdgeArray[StaticSkeleton] = ...

	#: underlying tree graph
	m_tree : Graph = ...

	#: type of nodes inT
	m_type : NodeArray[NodeType] = ...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates an SPQR treeTfor graphGrooted at the first edge ofG."""
		...

	@overload
	def __init__(self, G : Graph, e : edge) -> None:
		"""Creates an SPQR treeTfor graphGrooted at the edgee."""
		...

	@overload
	def __init__(self, G : Graph, tricComp : Triconnectivity) -> None:
		"""Creates an SPQR treeTfor graphGrooted at the first edge ofG."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def cpRec(self, v : node, Gp : PertinentGraph) -> None:
		"""Recursively performs the task of adding edges (and nodes) to the pertinent graphGpfor each involved skeleton graph."""
		...

	@overload
	def init(self, e : edge) -> None:
		"""Initialization(called by constructor)."""
		...

	@overload
	def init(self, eRef : edge, tricComp : Triconnectivity) -> None:
		"""Initialization(called by constructor)."""
		...

	def rootRec(self, v : node, ef : edge) -> None:
		"""Recursively performs rooting of tree."""
		...
