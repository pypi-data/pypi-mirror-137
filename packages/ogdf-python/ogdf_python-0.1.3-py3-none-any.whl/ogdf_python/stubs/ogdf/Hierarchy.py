# file stubs/ogdf/Hierarchy.py generated from classogdf_1_1_hierarchy
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Hierarchy(object):

	"""Representation of proper hierarchies used by Sugiyama-layout."""

	@overload
	def __init__(self) -> None:
		"""Creates an empty hierarchy."""
		...

	@overload
	def __init__(self, G : Graph, rank : NodeArray[  int ]) -> None:
		"""Creates an hierarchy of graphGwith node ranksrank."""
		...

	def __destruct__(self) -> None:
		...

	def createEmpty(self, G : Graph) -> None:
		...

	def initByNodes(self, nodes : List[node], eCopy : EdgeArray[edge], rank : NodeArray[  int ]) -> None:
		...

	def isLongEdgeDummy(self, v : node) -> bool:
		...

	def maxRank(self) -> int:
		...

	def __GraphCopy__(self) -> None:
		"""Conversion to constGraphCopyreference."""
		...

	def rank(self, v : node) -> int:
		"""Returns the rank (level) of nodev."""
		...

	def size(self, i : int) -> int:
		...
