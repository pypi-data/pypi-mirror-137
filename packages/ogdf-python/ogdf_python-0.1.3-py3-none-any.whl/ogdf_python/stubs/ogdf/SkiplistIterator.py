# file stubs/ogdf/SkiplistIterator.py generated from classogdf_1_1_skiplist_iterator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
X = TypeVar('X')

class SkiplistIterator(Generic[X]):

	"""Forward-Iterator for Skiplists."""

	def __ne__(self, other : SkiplistIterator[ X ]) -> bool:
		...

	def __deref__(self) -> X:
		"""Returns the item to which the iterator points."""
		...

	def __preinc__(self) -> SkiplistIterator[ X ]:
		"""Move the iterator one item forward (prefix notation)"""
		...

	def __postinc__(self, _ : int) -> SkiplistIterator[ X ]:
		"""Move the iterator one item forward (prefix notation)"""
		...

	def __eq__(self, other : SkiplistIterator[ X ]) -> bool:
		...

	def valid(self) -> bool:
		...
