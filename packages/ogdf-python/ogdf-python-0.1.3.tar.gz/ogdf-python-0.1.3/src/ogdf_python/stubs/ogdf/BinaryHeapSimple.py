# file stubs/ogdf/BinaryHeapSimple.py generated from classogdf_1_1_binary_heap_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
INDEX = TypeVar('INDEX')

X = TypeVar('X')

class BinaryHeapSimple(Generic[X, INDEX]):

	"""Dynamically growing binary heap tuned for efficiency on a small interface (compared toBinaryHeap)."""

	def __init__(self, size : INDEX) -> None:
		"""Construtor, giving initial array size."""
		...

	def clear(self) -> None:
		"""empties the heap [O(1)]"""
		...

	def empty(self) -> bool:
		"""Returns true if the heap is empty."""
		...

	def extractMin(self) -> X:
		"""Returns the top (i.e., smallest) element and removed it from the heap [Same aspop(), O(log n)]."""
		...

	def getMin(self) -> X:
		"""Returns a reference to the top (i.e., smallest) element of the heap. It does not remove it. [Same astop(), O(1)]."""
		...

	def insert(self, x : X) -> None:
		"""Adds an element to the heap [Same aspush(), O(log n)]."""
		...

	def __getitem__(self, idx : INDEX) -> X:
		"""obtain const references to the element at indexidx(the smallest array index is 0, as for traditional C-arrays)"""
		...

	def pop(self) -> X:
		"""Returns the top (i.e., smallest) element and removed it from the heap [Same asextractMin(), O(log n)]."""
		...

	def push(self, x : X) -> None:
		"""Adds an element to the heap [Same asinsert(), O(log n)]."""
		...

	def size(self) -> INDEX:
		"""Returns the number of elements in the heap."""
		...

	def top(self) -> X:
		"""Returns a reference to the top (i.e., smallest) element of the heap. It does not remove it. [Same asgetMin(), O(1)]."""
		...

	def capacity(self) -> INDEX:
		"""Returns the current array-size of the heap, i.e., the number of elements which can be added before the next resize occurs."""
		...

	def heapdown(self) -> None:
		...

	def heapup(self, idx : INDEX) -> None:
		...
