# file stubs/ogdf/HierarchyLevels.py generated from classogdf_1_1_hierarchy_levels
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
RNG = TypeVar('RNG')

class HierarchyLevels(ogdf.HierarchyLevelsBase):

	"""Representation of proper hierarchies used by Sugiyama-layout."""

	def __init__(self, H : Hierarchy) -> None:
		...

	def __destruct__(self) -> None:
		...

	def adjLevel(self, i : int) -> Level:
		"""Returns the adjacent level of leveli(according todirection())."""
		...

	@overload
	def adjNodes(self, v : node) -> Array[node]:
		"""Returns the adjacent nodes ofv(according todirection())."""
		...

	@overload
	def adjNodes(self, v : node, dir : TraversingDir) -> Array[node]:
		"""Returns the adjacent nodes ofv."""
		...

	@overload
	def buildAdjNodes(self) -> None:
		...

	@overload
	def buildAdjNodes(self, i : int) -> None:
		...

	@overload
	def calculateCrossingsSimDraw(self, edgeSubGraphs : EdgeArray[  int ]) -> int:
		"""Computes the total number of crossings (for simultaneous drawing)."""
		...

	@overload
	def calculateCrossingsSimDraw(self, i : int, edgeSubGraphs : EdgeArray[  int ]) -> int:
		"""Computes the number of crossings between leveliandi+1(for simultaneous drawing)."""
		...

	def check(self) -> None:
		...

	@overload
	def direction(self) -> TraversingDir:
		"""Returns the current direction of layer-by-layer sweep."""
		...

	@overload
	def direction(self, dir : TraversingDir) -> None:
		"""Sets the current direction of layer-by-layer sweep."""
		...

	def hierarchy(self) -> Hierarchy:
		...

	def high(self) -> int:
		"""Returns the maximal array index of a level (=size()-1)."""
		...

	@overload
	def __getitem__(self, i : int) -> Level:
		"""Returns thei-th level."""
		...

	@overload
	def __getitem__(self, i : int) -> Level:
		"""Returns thei-th level."""
		...

	@overload
	def permute(self) -> None:
		"""Permutes the order of nodes on each level."""
		...

	@overload
	def permute(self, rng : RNG) -> None:
		...

	def pos(self, v : node) -> int:
		"""Returns the position of nodevon its level."""
		...

	def print(self, os : std.ostream) -> None:
		...

	def restorePos(self, newPos : NodeArray[  int ]) -> None:
		"""Restores the position of nodes fromnewPos."""
		...

	def separateCCs(self, numCC : int, component : NodeArray[  int ]) -> None:
		"""Adjusts node positions such that nodes are ordered according to components numbers."""
		...

	def size(self) -> int:
		"""Returns the number of levels."""
		...

	def storePos(self, oldPos : NodeArray[  int ]) -> None:
		"""Stores the position of nodes inoldPos."""
		...

	def transpose(self, v : node) -> bool:
		...
