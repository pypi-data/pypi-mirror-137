# file stubs/ogdf/PairingHeapNode.py generated from structogdf_1_1_pairing_heap_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class PairingHeapNode(Generic[T]):

	"""Pairing heap node."""

	#: First child of the node.
	child : PairingHeapNode[ T ] = ...

	#: Next sibling of the node.
	next : PairingHeapNode[ T ] = ...

	#: Previous sibling of the node or parent.
	prev : PairingHeapNode[ T ] = ...

	#: Value contained in the node.
	value : T = ...

	def __init__(self, valueOfNode : T) -> None:
		"""Creates heap node with a givenvalueOfNode."""
		...
