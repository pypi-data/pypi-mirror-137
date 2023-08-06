# file stubs/ogdf/HierarchyLevelsBase.py generated from classogdf_1_1_hierarchy_levels_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HierarchyLevelsBase(object):

	class TraversingDir(enum.Enum):

		downward = enum.auto()

		upward = enum.auto()

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, _ : HierarchyLevelsBase) -> None:
		...

	def __destruct__(self) -> None:
		...

	def adjNodes(self, v : node, dir : TraversingDir) -> Array[node]:
		"""Returns the adjacent nodes ofv."""
		...

	@overload
	def calculateCrossings(self) -> int:
		"""Computes the total number of crossings."""
		...

	@overload
	def calculateCrossings(self, i : int) -> int:
		"""Computes the number of crossings between leveliandi+1."""
		...

	def hierarchy(self) -> Hierarchy:
		...

	def high(self) -> int:
		"""Returns the maximal array index of a level (=size()-1)."""
		...

	def __assign__(self, _ : HierarchyLevelsBase) -> HierarchyLevelsBase:
		...

	def __getitem__(self, i : int) -> LevelBase:
		"""Returns thei-th level."""
		...

	def pos(self, v : node) -> int:
		"""Returns the position of nodevon its level."""
		...

	def size(self) -> int:
		"""Returns the number of levels."""
		...
