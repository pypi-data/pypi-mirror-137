# file stubs/ogdf/HotQueue/__init__.py generated from classogdf_1_1_hot_queue
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
H = TypeVar('H')

P = TypeVar('P')

V = TypeVar('V')

class HotQueue(Generic[V, P, H]):

	"""Heap-on-Top queue implementation."""

	Handle : Type = HotQueueHandle[ V, P,HeapHandle]

	def __init__(self, change : P, levels : std.size_t) -> None:
		"""Creates empty Heap-on-Top queue."""
		...

	def __destruct__(self) -> None:
		"""Releases all buckets on destruction."""
		...

	def decrease(self, handle : Handle, priority : P) -> None:
		"""Decreases value of the givenhandletopriority."""
		...

	def empty(self) -> bool:
		"""Checks whether the heap is empty."""
		...

	def pop(self) -> None:
		"""Removes the top element from the heap."""
		...

	def push(self, value : V, priority : P) -> Handle:
		"""Inserts a new node with givenvalueandpriorityinto a heap."""
		...

	def size(self) -> std.size_t:
		"""Number of elements contained within the heap."""
		...

	def top(self) -> V:
		"""Returns reference to the top element in the heap."""
		...
