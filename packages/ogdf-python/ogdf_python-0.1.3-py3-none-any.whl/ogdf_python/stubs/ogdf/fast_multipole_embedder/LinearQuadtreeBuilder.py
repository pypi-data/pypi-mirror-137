# file stubs/ogdf/fast_multipole_embedder/LinearQuadtreeBuilder.py generated from classogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_builder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LinearQuadtreeBuilder(object):

	"""the builder for theLinearQuadtree"""

	firstInner : LinearQuadtree.NodeID = ...

	firstLeaf : LinearQuadtree.NodeID = ...

	lastInner : LinearQuadtree.NodeID = ...

	lastLeaf : LinearQuadtree.NodeID = ...

	n : LinearQuadtree.PointID = ...

	numInnerNodes : int = ...

	numLeaves : int = ...

	restoreChainLastNode : LinearQuadtree.NodeID = ...

	tree : LinearQuadtree = ...

	def __init__(self, treeRef : LinearQuadtree) -> None:
		"""constructor"""
		...

	def build(self) -> None:
		"""the main build call"""
		...

	@overload
	def buildHierarchy(self) -> None:
		"""the main function for the new link-only recursive builder"""
		...

	@overload
	def buildHierarchy(self, curr : LinearQuadtree.NodeID, maxLevel : int) -> LinearQuadtree.NodeID:
		"""the new link-only recursive builder"""
		...

	def CAL(self, a : LinearQuadtree.PointID, b : LinearQuadtree.PointID) -> int:
		"""returns the level of the first common ancestor of a and b"""
		...

	def mergeWithNext(self, curr : LinearQuadtree.NodeID) -> None:
		"""merges the node curr with curr's next node by appending the next nodes children to curr except the first one."""
		...

	def prepareNodeAndLeaf(self, leafPos : LinearQuadtree.PointID, nextLeafPos : LinearQuadtree.PointID) -> None:
		"""prepares the node and leaf layer at positionleafPoswherenextLeafPosis the next position"""
		...

	@overload
	def prepareTree(self) -> None:
		"""prepares the node and leaf layer for the complete tree from 0 to n (excluding n)"""
		...

	@overload
	def prepareTree(self, begin : LinearQuadtree.PointID, end : LinearQuadtree.PointID) -> None:
		"""prepares the node and leaf layer from position begin until end (excluding end)"""
		...

	@overload
	def restoreChain(self) -> None:
		...

	@overload
	def restoreChain(self, curr : LinearQuadtree.NodeID) -> None:
		...

	def restorePushBackChain(self, curr : LinearQuadtree.NodeID) -> None:
		"""used by restore chain"""
		...
