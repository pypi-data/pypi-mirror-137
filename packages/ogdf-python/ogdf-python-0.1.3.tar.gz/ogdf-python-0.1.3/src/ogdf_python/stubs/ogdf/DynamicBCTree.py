# file stubs/ogdf/DynamicBCTree.py generated from classogdf_1_1_dynamic_b_c_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicBCTree(ogdf.BCTree):

	"""Dynamic BC-trees."""

	def init(self) -> None:
		...

	def unite(self, uB : node, vB : node, wB : node) -> node:
		...

	def find(self, vB : node) -> node:
		"""The FIND function of the UNION/FIND structure."""
		...

	def parent(self, vB : node) -> node:
		...

	def condensePath(self, sG : node, tG : node) -> node:
		"""Performs path condensation."""
		...

	@overload
	def __init__(self, G : Graph, callInitConnected : bool = False) -> None:
		...

	@overload
	def __init__(self, G : Graph, vG : node, callInitConnected : bool = False) -> None:
		"""A constructor."""
		...

	@overload
	def bcproper(self, vG : node) -> node:
		...

	@overload
	def bcproper(self, eG : edge) -> node:
		"""Returns the BC-tree-vertex representing the biconnected component which a given edge of the original graph is belonging to."""
		...

	def repVertex(self, uG : node, vB : node) -> node:
		...

	def cutVertex(self, uB : node, vB : node) -> node:
		"""Returns the copy of a cut-vertex in the biconnected components graph which belongs to a certain B-component and leads to another B-component."""
		...

	def updateInsertedEdge(self, eG : edge) -> edge:
		...

	def updateInsertedNode(self, eG : edge, fG : edge) -> node:
		"""Update of the dynamic BC-tree after vertex insertion into the original graph."""
		...

	def insertEdge(self, sG : node, tG : node) -> edge:
		"""Inserts a new edge into the original graph and updates the BC-tree."""
		...

	def insertNode(self, eG : edge) -> node:
		"""Inserts a new vertex into the original graph and updates the BC-tree."""
		...

	def bComponent(self, uG : node, vG : node) -> node:
		...

	#: Arraythat contains for each proper BC-tree-vertex its degree.
	m_bNode_degree : NodeArray[  int ] = ...

	#: Arraythat contains for each BC-tree-vertex its parent in its UNION/FIND-tree structure.
	m_bNode_owner : NodeArray[node] = ...
