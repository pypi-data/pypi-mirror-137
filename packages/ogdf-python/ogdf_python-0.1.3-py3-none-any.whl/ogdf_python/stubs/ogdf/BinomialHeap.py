# file stubs/ogdf/BinomialHeap.py generated from classogdf_1_1_binomial_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

T = TypeVar('T')

class BinomialHeap(ogdf.HeapBase[ BinomialHeap[ T, std.less[ T ] ], BinomialHeapNode[ T ], T, std.less[ T ] ], Generic[T, C]):

	"""Binomial heap implementation."""

	def __init__(self, cmp : C = C(), initialSize : int = -1) -> None:
		"""Creates empty binomial heap."""
		...

	def __destruct__(self) -> None:
		"""Destructs the heap."""
		...

	def decrease(self, heapNode : BinomialHeapNode[ T ], value : T) -> None:
		"""Decreases value of the givenheapNodetovalue."""
		...

	def merge(self, other : BinomialHeap[ T, C ]) -> None:
		"""Merges in values ofotherheap."""
		...

	def pop(self) -> None:
		"""Removes the top element from the heap."""
		...

	def push(self, value : T) -> BinomialHeapNode[ T ]:
		"""Inserts a new node with givenvalueinto a heap."""
		...

	def top(self) -> T:
		"""Returns reference to the top element in the heap."""
		...

	def value(self, heapNode : BinomialHeapNode[ T ]) -> T:
		"""Returns the value of the node."""
		...
