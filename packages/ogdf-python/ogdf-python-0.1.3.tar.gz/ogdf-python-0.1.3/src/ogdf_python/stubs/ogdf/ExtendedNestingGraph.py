# file stubs/ogdf/ExtendedNestingGraph.py generated from classogdf_1_1_extended_nesting_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExtendedNestingGraph(ogdf.Graph):

	class NodeType(enum.Enum):

		Node = enum.auto()

		ClusterTop = enum.auto()

		ClusterBottom = enum.auto()

		Dummy = enum.auto()

		ClusterTopBottom = enum.auto()

	def __init__(self, CG : ClusterGraph) -> None:
		...

	def aeLevel(self, v : node) -> int:
		...

	def bottom(self, cOrig : cluster) -> node:
		...

	def bottomRank(self, c : cluster) -> int:
		...

	def chain(self, e : edge) -> List[edge]:
		...

	def copy(self, v : node) -> node:
		...

	def getClusterGraph(self) -> ClusterGraphCopy:
		...

	def getOriginalClusterGraph(self) -> ClusterGraph:
		...

	def isLongEdgeDummy(self, v : node) -> bool:
		...

	def isReversed(self, e : edge) -> bool:
		...

	def isVirtual(self, c : cluster) -> bool:
		...

	def layer(self, i : int) -> ENGLayer:
		...

	def layerHierarchyTree(self, i : int) -> LHTreeNode:
		...

	def numberOfLayers(self) -> int:
		...

	def origEdge(self, e : edge) -> edge:
		...

	def originalCluster(self, v : node) -> cluster:
		...

	def origNode(self, v : node) -> node:
		...

	@overload
	def parent(self, c : cluster) -> cluster:
		...

	@overload
	def parent(self, v : node) -> cluster:
		...

	def permute(self) -> None:
		...

	def pos(self, v : node) -> int:
		...

	def rank(self, v : node) -> int:
		...

	@overload
	def reduceCrossings(self, i : int, dirTopDown : bool) -> RCCrossings:
		...

	def removeTopBottomEdges(self) -> None:
		...

	def restorePos(self) -> None:
		...

	def storeCurrentPos(self) -> None:
		...

	def top(self, cOrig : cluster) -> node:
		...

	def topRank(self, c : cluster) -> int:
		...

	def type(self, v : node) -> NodeType:
		...

	def verticalSegment(self, e : edge) -> bool:
		...

	def addEdge(self, u : node, v : node, addAlways : bool = False) -> edge:
		...

	def assignAeLevel(self, c : cluster, count : int) -> None:
		...

	def assignPos(self, vNode : LHTreeNode, count : int) -> None:
		...

	@overload
	def lca(self, uNode : LHTreeNode, vNode : LHTreeNode, uChild : LHTreeNode, vChild : LHTreeNode) -> LHTreeNode:
		...

	@overload
	def lca(self, u : node, v : node) -> cluster:
		...

	def moveDown(self, v : node, successors : SListPure[node], level : NodeArray[  int ]) -> None:
		...

	def reachable(self, v : node, u : node, successors : SListPure[node]) -> bool:
		...

	@overload
	def reduceCrossings(self, cNode : LHTreeNode, dirTopDown : bool) -> RCCrossings:
		...

	def tryEdge(self, u : node, v : node, G : Graph, level : NodeArray[  int ]) -> bool:
		...
