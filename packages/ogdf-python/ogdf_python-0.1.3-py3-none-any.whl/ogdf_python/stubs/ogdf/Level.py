# file stubs/ogdf/Level.py generated from classogdf_1_1_level
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

class Level(ogdf.LevelBase):

	"""Representation of levels in hierarchies."""

	def __init__(self, pLevels : HierarchyLevels, index : int, num : int) -> None:
		"""Creates a level with indexindexin hierarchypLevels."""
		...

	def __destruct__(self) -> None:
		...

	def adjNodes(self, v : node) -> Array[node]:
		"""Returns the (sorted) array of adjacent nodes ofv(according to direction())."""
		...

	def high(self) -> int:
		"""Returns the maximal array index (=size()-1)."""
		...

	def index(self) -> int:
		"""Returns the array index of this level in the hierarchy."""
		...

	def levels(self) -> HierarchyLevels:
		"""Returns the hierarchy to which this level belongs."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the node at positioni."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the node at positioni."""
		...

	def recalcPos(self) -> None:
		...

	def size(self) -> int:
		"""Returns the number of nodes on this level."""
		...

	@overload
	def sort(self, weight : NodeArray[ float ]) -> None:
		"""Sorts the nodes according toweightusing quicksort."""
		...

	@overload
	def sort(self, weight : NodeArray[  int ], minBucket : int, maxBucket : int) -> None:
		"""Sorts the nodes according toweightusing bucket sort."""
		...

	def sortByWeightOnly(self, weight : NodeArray[ float ]) -> None:
		"""Sorts the nodes according toweight(without special placement for "isolated" nodes)."""
		...

	def sortOrder(self, orderComparer : C) -> None:
		"""Sorts the nodes according toorderComparer."""
		...

	def swap(self, i : int, j : int) -> None:
		"""Exchanges nodes at positioniandj."""
		...
