# file stubs/ogdf/Skiplist/__init__.py generated from classogdf_1_1_skiplist
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
X = TypeVar('X')

class Skiplist(Generic[X]):

	"""A randomized skiplist."""

	def __init__(self) -> None:
		"""Construct an initially empty skiplist."""
		...

	def __destruct__(self) -> None:
		...

	def add(self, item : X) -> None:
		"""Adds the itemiteminto the skiplist [O'(log n)]."""
		...

	def begin(self) -> SkiplistIterator[ X ]:
		"""returns an (forward) iterator for the skiplist"""
		...

	def clear(self, killData : bool = False) -> None:
		"""Clears the current skiplist."""
		...

	def empty(self) -> bool:
		"""Returns true if the skiplist contains no elements."""
		...

	def end(self) -> SkiplistIterator[ X ]:
		"""returns an invalid iterator"""
		...

	def isElement(self, item : X) -> bool:
		"""Returns true if the itemitemis contained in the skiplist [O'(log n)]."""
		...

	def size(self) -> int:
		"""Returns the current size of the skiplist, i.e., the number of elements."""
		...
