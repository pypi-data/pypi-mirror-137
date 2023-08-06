# file stubs/ogdf/LHTreeNode/__init__.py generated from classogdf_1_1_l_h_tree_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LHTreeNode(object):

	class Type(enum.Enum):

		Compound = enum.auto()

		Node = enum.auto()

		AuxNode = enum.auto()

	m_lowerAdj : List[Adjacency] = ...

	m_lowerClusterCrossing : List[ClusterCrossing] = ...

	m_upperAdj : List[Adjacency] = ...

	m_upperClusterCrossing : List[ClusterCrossing] = ...

	@overload
	def __init__(self, c : cluster, up : LHTreeNode) -> None:
		...

	@overload
	def __init__(self, parent : LHTreeNode, v : node, t : Type = Type.Node) -> None:
		...

	@overload
	def child(self, i : int) -> LHTreeNode:
		...

	@overload
	def child(self, i : int) -> LHTreeNode:
		...

	def down(self) -> LHTreeNode:
		...

	def getNode(self) -> node:
		...

	def initChild(self, n : int) -> None:
		...

	def isCompound(self) -> bool:
		...

	def numberOfChildren(self) -> int:
		...

	def originalCluster(self) -> cluster:
		...

	@overload
	def parent(self) -> LHTreeNode:
		...

	@overload
	def parent(self) -> LHTreeNode:
		...

	def permute(self) -> None:
		...

	def pos(self) -> int:
		...

	def removeAuxChildren(self) -> None:
		...

	def restore(self) -> None:
		...

	def setChild(self, i : int, p : LHTreeNode) -> None:
		...

	def setParent(self, p : LHTreeNode) -> None:
		...

	def setPos(self) -> None:
		...

	def store(self) -> None:
		...

	def up(self) -> LHTreeNode:
		...
