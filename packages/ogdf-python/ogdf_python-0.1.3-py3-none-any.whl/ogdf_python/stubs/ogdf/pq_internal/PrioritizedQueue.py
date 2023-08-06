# file stubs/ogdf/pq_internal/PrioritizedQueue.py generated from classogdf_1_1pq__internal_1_1_prioritized_queue
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

Impl = TypeVar('Impl')

P = TypeVar('P')

E = TypeVar('E')

class PrioritizedQueue(ogdf.PriorityQueue[ E, P, C, Impl ], Generic[E, P, C, Impl]):

	"""Defines a queue for handling prioritized elements."""

	#: The type of handle for accessing the elements of this queue.
	Handle : Type = SuperQueue.handle

	def __init__(self, cmp : C = C(), initialSize : int = 128) -> None:
		...

	def decrease(self, pos : Handle, priority : P) -> None:
		...

	def push(self, element : E, priority : P) -> Handle:
		"""Pushes a new element with the respective priority to the queue."""
		...

	def topElement(self) -> E:
		"""Returns the topmost element in the queue."""
		...

	def topPriority(self) -> P:
		"""Returns the priority of the topmost element in this queue."""
		...
