# file stubs/ogdf/HotQueueNode.py generated from structogdf_1_1_hot_queue_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
P = TypeVar('P')

V = TypeVar('V')

class HotQueueNode(Generic[V, P]):

	"""Heap-on-Top bucket element."""

	next : HotQueueNode[ V, P ] = ...

	prev : HotQueueNode[ V, P ] = ...

	priority : P = ...

	value : V = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, val : V, pr : P) -> None:
		...
