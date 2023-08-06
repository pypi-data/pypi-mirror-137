# file stubs/ogdf/BlockOrder.py generated from classogdf_1_1_block_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BlockOrder(ogdf.HierarchyLevelsBase):

	"""Hierarchical graph representation used byGlobalSiftingandGridSiftingalgorithms."""

	# HierarchyLevelsBase members

	def __getitem__(self, i : int) -> ArrayLevel:
		"""Returns thei-th level."""
		...

	def pos(self, v : node) -> int:
		"""Returns the position of nodevon its level."""
		...

	def size(self) -> int:
		"""Returns the number of levels."""
		...

	def hierarchy(self) -> Hierarchy:
		...

	def adjNodes(self, v : node, dir : TraversingDir) -> Array[node]:
		"""Returns the adjacent nodes ofv."""
		...

	# GridSifting

	m_verticalStepsBound : int = ...

	def gridSifting(self, nRepeats : int = 10) -> None:
		"""Calls the grid sifting algorithm on a graph (its hierarchy)."""
		...

	def __init__(self, hierarchy : Hierarchy, longEdgesOnly : bool = True) -> None:
		...

	def __destruct__(self) -> None:
		...

	def blocksCount(self) -> int:
		"""Returns the number of blocks."""
		...

	def globalSifting(self, rho : int = 1, nRepeats : int = 10, pNumCrossings : int = None) -> None:
		"""Calls the global sifting algorithm on graph (its hierarchy)."""
		...
