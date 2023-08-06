# file stubs/ogdf/HeapBase.py generated from classogdf_1_1_heap_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

H = TypeVar('H')

IMPL = TypeVar('IMPL')

C = TypeVar('C')

class HeapBase(Generic[IMPL, H, T, C]):

	"""Common interface for all heap classes."""

	#: The type of handle used to identify stored values.
	Handle : Type = H

	def __init__(self, comp : C = C()) -> None:
		...

	def comparator(self) -> C:
		"""Returns the comparator used to sort the values in the heap."""
		...

	def decrease(self, handle : Handle, value : T) -> None:
		"""Decreases a single value."""
		...

	def merge(self, other : IMPL) -> None:
		"""Merges in values ofotherheap."""
		...

	def pop(self) -> None:
		"""Removes the topmost value from the heap."""
		...

	def push(self, value : T) -> Handle:
		"""Inserts a value into the heap."""
		...

	def top(self) -> T:
		"""Returns the topmost value in the heap."""
		...

	def value(self, handle : Handle) -> T:
		"""Returns the value of that handle."""
		...
