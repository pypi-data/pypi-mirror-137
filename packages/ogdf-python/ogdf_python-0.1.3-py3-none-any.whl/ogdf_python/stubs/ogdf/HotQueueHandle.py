# file stubs/ogdf/HotQueueHandle.py generated from structogdf_1_1_hot_queue_handle
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
P = TypeVar('P')

V = TypeVar('V')

HeapHandle = TypeVar('HeapHandle')

class HotQueueHandle(Generic[V, P, HeapHandle]):

	"""Heap-on-Top handle to inserted items."""

	#: Handle to bucket element (bucket index and list iterator).
	bucketHandle : std.pair[ std.size_t,HotQueueNode[ V, P ]  ] = ...

	#: Handle to underlying heap.
	heapHandle : HeapHandle = ...

	def __init__(self, other : HotQueueHandle) -> None:
		...

	def __assign__(self, other : HotQueueHandle) -> HotQueueHandle:
		...
