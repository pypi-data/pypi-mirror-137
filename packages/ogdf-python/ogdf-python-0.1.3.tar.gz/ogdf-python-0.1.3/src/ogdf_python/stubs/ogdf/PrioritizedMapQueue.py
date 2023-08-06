# file stubs/ogdf/PrioritizedMapQueue.py generated from classogdf_1_1_prioritized_map_queue_3_01node_00_01_p_00_01_c_00_01_impl_00_01_hash_func_01_4
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

HashFunc = TypeVar('HashFunc')

Impl = TypeVar('Impl')

P = TypeVar('P')

class PrioritizedMapQueue(ogdf.pq_internal.PrioritizedArrayQueueBase[ node, P, C, Impl, NodeArray[ PrioritizedQueue[ node, P, C, Impl ].Handle ] ], Generic[P, C, Impl, HashFunc]):

	"""Specialization fornodeelements."""

	def __init__(self, G : Graph, cmp : C = C(), initialSize : int = -1) -> None:
		"""Creates a new queue with the given comparer."""
		...

	def clear(self) -> None:
		"""Removes all elements from this queue."""
		...
