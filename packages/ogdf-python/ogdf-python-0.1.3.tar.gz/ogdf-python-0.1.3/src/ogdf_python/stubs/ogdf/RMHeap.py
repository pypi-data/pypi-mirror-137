# file stubs/ogdf/RMHeap.py generated from classogdf_1_1_r_m_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

T = TypeVar('T')

class RMHeap(ogdf.HeapBase[ RMHeap[ T, std.less[ T ] ], RMHeapNode[ T ], T, std.less[ T ] ], Generic[T, C]):

	"""Randomized meldable heap implementation."""

	def __init__(self, cmp : C = C(), initialSize : int = -1) -> None:
		"""Creates empty randomized meldable heap."""
		...

	def __destruct__(self) -> None:
		"""Destructs the heap."""
		...

	def decrease(self, heapNode : RMHeapNode[ T ], value : T) -> None:
		"""Decreases value of the givenheapNodetovalue."""
		...

	def merge(self, other : RMHeap[ T, C ]) -> None:
		"""Merges in values ofotherheap."""
		...

	def pop(self) -> None:
		"""Removes the top element from the heap."""
		...

	def push(self, value : T) -> RMHeapNode[ T ]:
		"""Inserts a new node with givenvalueinto a heap."""
		...

	def top(self) -> T:
		"""Returns reference to the top element in the heap."""
		...

	def value(self, heapNode : RMHeapNode[ T ]) -> T:
		"""Returns the value of the node."""
		...
