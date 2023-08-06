# file stubs/ogdf/Skeleton.py generated from classogdf_1_1_skeleton
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Skeleton(object):

	"""Skeleton graphs of nodes in an SPQR-tree."""

	#: actual skeleton graph
	m_M : Graph = ...

	#: reference edge
	m_referenceEdge : edge = ...

	#: corresp.
	m_treeNode : node = ...

	def __init__(self, vT : node) -> None:
		"""Creates a skeletonSwith owner treeTand corresponding nodevT."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def getGraph(self) -> Graph:
		"""Returns a reference to the skeleton graphM."""
		...

	@overload
	def getGraph(self) -> Graph:
		"""Returns a reference to the skeleton graphM."""
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

	def referenceEdge(self) -> edge:
		"""Returns the reference edge ofSinM."""
		...

	def treeNode(self) -> node:
		"""Returns the corresponding node in the owner treeTto whichSbelongs."""
		...

	def twinEdge(self, e : edge) -> edge:
		"""Returns the twin edge of skeleton edgee."""
		...

	def twinTreeNode(self, e : edge) -> node:
		"""Returns the tree node in T containing the twin edge of skeleton edgee."""
		...
