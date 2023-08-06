# file stubs/ogdf/PairingHeap.py generated from classogdf_1_1_pairing_heap
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

T = TypeVar('T')

class PairingHeap(ogdf.HeapBase[ PairingHeap[ T, C ], PairingHeapNode[ T ], T, C ], Generic[T, C]):

	"""Pairing heap implementation."""

	def __init__(self, cmp : C = C(), initialSize : int = -1) -> None:
		"""Creates empty pairing heap."""
		...

	def __destruct__(self) -> None:
		"""Destructs pairing heap."""
		...

	def decrease(self, heapNode : PairingHeapNode[ T ], value : T) -> None:
		"""Decreases value of the givenheapNodetovalue."""
		...

	def merge(self, other : PairingHeap[ T, C ]) -> None:
		"""Merges in values ofotherheap."""
		...

	def pop(self) -> None:
		"""Removes the top element from the heap."""
		...

	def push(self, value : T) -> PairingHeapNode[ T ]:
		"""Inserts a new node with givenvalueinto a heap."""
		...

	def top(self) -> T:
		"""Returns reference to the top element in the heap."""
		...

	def value(self, heapNode : PairingHeapNode[ T ]) -> T:
		"""Returns the value of the node."""
		...
