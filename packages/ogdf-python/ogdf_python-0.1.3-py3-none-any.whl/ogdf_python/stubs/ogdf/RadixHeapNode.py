# file stubs/ogdf/RadixHeapNode.py generated from classogdf_1_1_radix_heap_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
P = TypeVar('P')

V = TypeVar('V')

class RadixHeapNode(Generic[V, P]):

	next : RadixHeapNode[ V, P ] = ...

	prev : RadixHeapNode[ V, P ] = ...

	priority : P = ...

	value : V = ...

	def __init__(self, nodeValue : V, nodePriority : P) -> None:
		...
