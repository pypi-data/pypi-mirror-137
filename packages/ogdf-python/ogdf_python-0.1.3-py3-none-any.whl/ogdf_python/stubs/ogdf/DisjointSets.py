# file stubs/ogdf/DisjointSets.py generated from classogdf_1_1_disjoint_sets
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
linkOption = TypeVar('linkOption')

compressionOption = TypeVar('compressionOption')

interleavingOption = TypeVar('interleavingOption')

class DisjointSets(Generic[linkOption, compressionOption, interleavingOption]):

	"""A Union/Find data structure for maintaining disjoint sets."""

	@overload
	def __init__(self, _ : DisjointSets) -> None:
		...

	@overload
	def __init__(self, maxNumberOfElements : int = (1<< 15)) -> None:
		"""Creates an emptyDisjointSetsstructure."""
		...

	def __destruct__(self) -> None:
		...

	def find(self, set : int) -> int:
		"""Returns the id of the largest superset ofsetand compresses the path according toCompressionOptions."""
		...

	def getNumberOfElements(self) -> int:
		"""Returns the current number of elements."""
		...

	def getNumberOfSets(self) -> int:
		"""Returns the current number of disjoint sets."""
		...

	def getRepresentative(self, set : int) -> int:
		"""Returns the id of the largest superset ofset."""
		...

	@overload
	def init(self) -> None:
		"""Resets theDisjointSetsstructure to be empty, preserving the previous value of maxNumberOfElements."""
		...

	@overload
	def init(self, maxNumberOfElements : int) -> None:
		"""Resets theDisjointSetsstructure to be empty, also changing the expected number of elements."""
		...

	def link(self, set1 : int, set2 : int) -> int:
		"""Unionsset1andset2."""
		...

	def makeSet(self) -> int:
		"""Initializes a singleton set."""
		...

	def __assign__(self, _ : DisjointSets) -> DisjointSets:
		...

	def quickUnion(self, set1 : int, set2 : int) -> bool:
		"""Unions the maximal disjoint sets containingset1andset2."""
		...
