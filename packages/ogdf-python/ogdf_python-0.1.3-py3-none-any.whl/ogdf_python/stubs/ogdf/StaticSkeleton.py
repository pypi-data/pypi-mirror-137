# file stubs/ogdf/StaticSkeleton.py generated from classogdf_1_1_static_skeleton
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StaticSkeleton(ogdf.Skeleton):

	"""Skeleton graphs of nodes in a static SPQR-tree."""

	#: corresp.
	m_orig : NodeArray[node] = ...

	#: owner tree
	m_owner : StaticSPQRTree = ...

	#: corresp.
	m_real : EdgeArray[edge] = ...

	#: corresp.
	m_treeEdge : EdgeArray[edge] = ...

	def __init__(self, T : StaticSPQRTree, vT : node) -> None:
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

	def treeEdge(self, e : edge) -> edge:
		"""Returns the tree edge which is associated with skeleton edgee."""
		...

	def twinEdge(self, e : edge) -> edge:
		"""Returns the twin edge of skeleton edgee."""
		...

	def twinTreeNode(self, e : edge) -> node:
		"""Returns the tree node in T containing the twin edge of skeleton edgee."""
		...
