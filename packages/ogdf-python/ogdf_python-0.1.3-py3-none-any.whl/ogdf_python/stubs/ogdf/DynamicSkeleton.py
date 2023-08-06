# file stubs/ogdf/DynamicSkeleton.py generated from classogdf_1_1_dynamic_skeleton
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicSkeleton(ogdf.Skeleton):

	"""Skeleton graphs of nodes in a dynamic SPQR-tree."""

	#: corresp.
	m_origEdge : EdgeArray[edge] = ...

	#: corresp.
	m_origNode : NodeArray[node] = ...

	#: owner tree
	m_owner : DynamicSPQRTree = ...

	def __init__(self, T : DynamicSPQRTree, vT : node) -> None:
		"""Creates a skeletonSwith owner treeTand corresponding nodevT."""
		...

	def __destruct__(self) -> None:
		...

	def isVirtual(self, e : edge) -> bool:
		"""Returns true iffeis a virtual edge."""
		...

	def original(self, v : node) -> node:
		"""Returns the vertex in the original graphGthat corresponds tov."""
		...

	def owner(self) -> SPQRTree:
		"""Returns the owner treeT."""
		...

	def realEdge(self, e : edge) -> edge:
		"""Returns the real edge that corresponds to skeleton edgee."""
		...

	def twinEdge(self, e : edge) -> edge:
		"""Returns the twin edge of skeleton edgee."""
		...

	def twinTreeNode(self, e : edge) -> node:
		"""Returns the tree node in T containing the twin edge of skeleton edgee."""
		...
