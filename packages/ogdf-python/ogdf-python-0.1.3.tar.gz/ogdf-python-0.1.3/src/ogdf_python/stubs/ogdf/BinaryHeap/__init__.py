# file stubs/ogdf/BinaryHeap/__init__.py generated from classogdf_1_1_binary_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

T = TypeVar('T')

class BinaryHeap(ogdf.HeapBase[ BinaryHeap[ T, std.less[ T ] ],  int, T, std.less[ T ] ], Generic[T, C]):

	"""Heap realized by a data array."""

	def __init__(self, comp : C = C(), initialSize : int = 128) -> None:
		"""Initializes an empty binary heap."""
		...

	def __destruct__(self) -> None:
		...

	def capacity(self) -> int:
		"""Returns the current size."""
		...

	def clear(self) -> None:
		"""Reinitializes the data structure."""
		...

	def decrease(self, handle : int, value : T) -> None:
		"""Decreases a single value."""
		...

	def empty(self) -> bool:
		"""Returns true iff the heap is empty."""
		...

	def pop(self) -> None:
		"""Removes the topmost value from the heap."""
		...

	def push(self, value : T) -> int:
		"""Inserts a value into the heap."""
		...

	def size(self) -> int:
		"""Returns the number of stored elements."""
		...

	def top(self) -> T:
		"""Returns the topmost value in the heap."""
		...

	def value(self, handle : int) -> T:
		"""Returns the value of that handle."""
		...
