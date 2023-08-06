# file stubs/ogdf/Top10Heap.py generated from classogdf_1_1_top10_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
INDEX = TypeVar('INDEX')

X = TypeVar('X')

class Top10Heap(ogdf.BinaryHeapSimple[ X,  int ], Generic[X, INDEX]):

	"""A variant ofBinaryHeapSimplewhich always holds only the X (e.g. X=10) elements with the highest keys."""

	class PushResult(enum.Enum):

		"""The type for results of aTop10Heap::pushoperation."""

		Accepted = enum.auto()

		Rejected = enum.auto()

		Swapped = enum.auto()

	def returnedSomething(self, r : PushResult) -> bool:
		"""Convenience function: Returns true if the PushResults states that push caused an element to be not/no-longer in the heap."""
		...

	def successful(self, r : PushResult) -> bool:
		"""Convenience function: Returns true if the PushResults states that the newly pushed element is new in the heap."""
		...

	def __init__(self) -> None:
		"""Constructor generating a heap which holds the 10 elements with highest value ever added to the heap."""
		...

	def full(self) -> bool:
		"""Returns true if the heap is completely filled (i.e. the next push operation will return something)"""
		...

	def insert(self, x : X, out : X) -> PushResult:
		"""Alternative name forpush()."""
		...

	def insertBlind(self, x : X) -> None:
		"""Alternative name forpushBlind()."""
		...

	def __getitem__(self, idx : INDEX) -> X:
		"""obtain const references to the element at indexidx"""
		...

	def push(self, x : X, out : X) -> PushResult:
		"""Tries to push the elementxonto the heap (and may return a removed element asout)."""
		...

	def pushBlind(self, x : X) -> None:
		"""Simple (and slightly faster) variant ofTop10Heap::push."""
		...
