# file stubs/ogdf/RadixHeap.py generated from classogdf_1_1_radix_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
P = TypeVar('P')

V = TypeVar('V')

class RadixHeap(Generic[V, P]):

	"""Radix heap data structure implementation."""

	def __init__(self) -> None:
		"""Creates empty heap."""
		...

	def __destruct__(self) -> None:
		"""Destructs the heap."""
		...

	def empty(self) -> bool:
		"""Checks whether the heap is empty."""
		...

	def pop(self) -> V:
		"""Removes the top element from the heap and returns its value."""
		...

	def push(self, value : V, priority : P) -> RadixHeapNode[ V, P ]:
		"""Inserts a new node with givenvalueandpriorityinto a heap."""
		...

	def size(self) -> std.size_t:
		"""Number of elements contained within the heap."""
		...
