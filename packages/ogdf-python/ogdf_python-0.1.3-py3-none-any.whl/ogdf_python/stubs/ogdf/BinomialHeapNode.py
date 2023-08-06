# file stubs/ogdf/BinomialHeapNode.py generated from structogdf_1_1_binomial_heap_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class BinomialHeapNode(Generic[T]):

	"""Binomial heap node."""

	#: First child of the node.
	child : BinomialHeapNode[ T ] = ...

	#: Next sibling of the node.
	next : BinomialHeapNode[ T ] = ...

	#: Parent of the node.
	parent : BinomialHeapNode[ T ] = ...

	#: Determines rank of a node.
	rank : size_t = ...

	#: Value contained in the node.
	value : T = ...

	def __init__(self, nodeValue : T) -> None:
		"""Creates heap node with a givennodeValue."""
		...
