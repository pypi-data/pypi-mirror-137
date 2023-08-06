# file stubs/ogdf/fast_multipole_embedder/FMELocalContext.py generated from structogdf_1_1fast__multipole__embedder_1_1_f_m_e_local_context
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMELocalContext(object):

	"""Local thread Context."""

	#: local maximum force
	avgForce : float = ...

	currAvgEdgeLength : float = ...

	#: first inner nodes the thread prepared
	firstInnerNode : LinearQuadtree.NodeID = ...

	#: first leaves the thread prepared
	firstLeaf : LinearQuadtree.NodeID = ...

	#: local force array for all nodes, points
	forceX : float = ...

	#: local force array for all nodes, points
	forceY : float = ...

	#: chain of inner nodes assigned to the thread
	innerNodePartition : FMENodeChainPartition = ...

	#: last inner nodes the thread prepared
	lastInnerNode : LinearQuadtree.NodeID = ...

	#: last leaves the thread prepared
	lastLeaf : LinearQuadtree.NodeID = ...

	#: chain of leaf nodes assigned to the thread
	leafPartition : FMENodeChainPartition = ...

	#: global point, node max x coordinate for bounding box calculations
	max_x : float = ...

	#: global point, node max y coordinate for bounding box calculations
	max_y : float = ...

	#: local maximum force
	maxForceSq : float = ...

	#: global point, node min x coordinate for bounding box calculations
	min_x : float = ...

	#: global point, node min y coordinate for bounding box calculations
	min_y : float = ...

	#: number of inner nodes the thread prepared
	numInnerNodes : int = ...

	#: number of leaves the thread prepared
	numLeaves : int = ...

	#: pointer to the global context
	pGlobalContext : FMEGlobalContext = ...

	#: tree partition assigned to the thread
	treePartition : FMETreePartition = ...
