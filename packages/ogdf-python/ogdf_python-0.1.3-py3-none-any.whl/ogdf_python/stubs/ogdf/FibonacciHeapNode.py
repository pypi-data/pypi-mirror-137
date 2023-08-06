# file stubs/ogdf/FibonacciHeapNode.py generated from structogdf_1_1_fibonacci_heap_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FibonacciHeapNode(Generic[T]):

	"""Fibonacci heap node."""

	#: First child of the node.
	child : FibonacciHeapNode[ T ] = ...

	#: Indicates whether node is marked or not.
	marked : bool = ...

	#: Next sibling of the node.
	next : FibonacciHeapNode[ T ] = ...

	#: Parent of the node.
	parent : FibonacciHeapNode[ T ] = ...

	#: Previous sibling of the node.
	prev : FibonacciHeapNode[ T ] = ...

	#: Determines rank of a node.
	rank : size_t = ...

	#: Value contained in the node.
	value : T = ...

	@overload
	def __init__(self) -> None:
		"""Creates empty root node."""
		...

	@overload
	def __init__(self, nodeValue : T) -> None:
		"""Creates heap node with a givennodeValue."""
		...
