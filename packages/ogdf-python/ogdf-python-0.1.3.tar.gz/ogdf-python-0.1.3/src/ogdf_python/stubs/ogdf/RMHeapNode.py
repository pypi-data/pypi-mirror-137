# file stubs/ogdf/RMHeapNode.py generated from structogdf_1_1_r_m_heap_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class RMHeapNode(Generic[T]):

	"""Randomized meldable heap node."""

	#: Left child of the node.
	left : RMHeapNode[ T ] = ...

	#: Parent of the node.
	parent : RMHeapNode[ T ] = ...

	#: Right child of the node.
	right : RMHeapNode[ T ] = ...

	#: Value contained in the node.
	value : T = ...

	def __init__(self, nodeValue : T) -> None:
		"""Creates heap node with a givennodeValue."""
		...
