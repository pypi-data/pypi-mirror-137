# file stubs/ogdf/DeletingTop10Heap.py generated from classogdf_1_1_deleting_top10_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Priority = TypeVar('Priority')

INDEX = TypeVar('INDEX')

STATICCOMPARER = TypeVar('STATICCOMPARER')

X = TypeVar('X')

class DeletingTop10Heap(ogdf.Top10Heap[ Prioritized[ X , float ],  int ], Generic[X, Priority, STATICCOMPARER, INDEX]):

	"""A variant ofTop10Heapwhich deletes the elements that get rejected from the heap."""

	def __init__(self, size : int) -> None:
		"""Construct aDeletingTop10Heapof given maximal capacity."""
		...

	def insertAndDelete(self, x : X, p : Priority) -> None:
		"""Alternative name forpushAndDelete()."""
		...

	def insertAndDeleteNoRedundancy(self, x : X, p : Priority) -> None:
		"""Alternative name for pushAndKillNoRedundancy()."""
		...

	def pushAndDelete(self, x : X, p : Priority) -> None:
		"""Inserts the elementxinto the heap with prioritypand deletes the element with smallest priority if the heap is full."""
		...

	def pushAndDeleteNoRedundancy(self, x : X, p : Priority) -> None:
		"""Analogous to pushandDelete(), but furthermore rejects (and deletes) an element if an equal element is already in the heap."""
		...
