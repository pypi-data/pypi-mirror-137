# file stubs/ogdf/fast_multipole_embedder/WSPD.py generated from classogdf_1_1fast__multipole__embedder_1_1_w_s_p_d
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class WSPD(object):

	"""Class for the Well-Separated-Pairs-Decomposition (WSPD)"""

	NodeID : Type = LinearQuadtree.NodeID

	def __init__(self, maxNumNodes : int) -> None:
		"""Constructor. Allocates the memory via OGDF_MALLOC_16."""
		...

	def __destruct__(self) -> None:
		"""Destructor. Deallocates via OGDF_FREE_16."""
		...

	def addWSP(self, a : NodeID, b : NodeID) -> None:
		"""Adds a well separated pair (a,b)"""
		...

	def clear(self) -> None:
		"""Resets the arraym_nodeInfo."""
		...

	def firstPairEntry(self, nodeID : NodeID) -> int:
		"""Returns the index of the first pair of nodenodeID."""
		...

	def maxNumNodes(self) -> int:
		"""Returns the maximum number of nodes. Equals the maximum number of nodes in theLinearQuadtree."""
		...

	def maxNumPairs(self) -> int:
		"""Returns the maximum number of pairs."""
		...

	def nextPair(self, currPairIndex : int, a : NodeID) -> int:
		"""Returns the index of the next pair ofcurrPairIndexof the node with indexa."""
		...

	def nodeInfo(self, nodeID : NodeID) -> NodeAdjInfo:
		"""Returns the node info for indexnodeID."""
		...

	def numPairs(self) -> int:
		"""Returns the total number of pairs."""
		...

	def numWSNodes(self, a : NodeID) -> int:
		"""Returns the number of well separated nodes for nodea."""
		...

	def pairInfo(self, pairIndex : int) -> EdgeAdjInfo:
		"""Returns the pair info for indexpairIndex."""
		...

	def sizeInBytes(self) -> int:
		...

	def wsNodeOfPair(self, currPairIndex : int, a : NodeID) -> int:
		"""Returns the other node (nota) of the pair with indexcurrPairIndex."""
		...
