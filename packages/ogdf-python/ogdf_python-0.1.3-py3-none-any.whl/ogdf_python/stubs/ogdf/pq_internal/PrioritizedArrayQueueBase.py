# file stubs/ogdf/pq_internal/PrioritizedArrayQueueBase.py generated from classogdf_1_1pq__internal_1_1_prioritized_array_queue_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

Impl = TypeVar('Impl')

Map = TypeVar('Map')

P = TypeVar('P')

E = TypeVar('E')

class PrioritizedArrayQueueBase(ogdf.pq_internal.PrioritizedQueue[ E, P, C, Impl ], Generic[E, P, C, Impl, Map]):

	Handle : Type = PrioritizedQueue[ E, P, C, Impl ].Handle

	SuperQueue : Type = PrioritizedQueue[ E, P, C, Impl ]

	m_handles : Map = ...

	def clear(self) -> None:
		"""Removes all elements from this queue."""
		...

	def contains(self, element : E) -> bool:
		"""Returns whether this queue contains that key."""
		...

	def decrease(self, element : E, priority : P) -> None:
		"""Decreases the priority of the given element."""
		...

	def pop(self) -> None:
		"""Removes the topmost element from the queue."""
		...

	def priority(self, element : E) -> P:
		...

	def push(self, element : E, priority : P) -> None:
		"""Adds a new element to the queue."""
		...

	def __init__(self, cmp : C, initialSize : int, map : Map) -> None:
		...
