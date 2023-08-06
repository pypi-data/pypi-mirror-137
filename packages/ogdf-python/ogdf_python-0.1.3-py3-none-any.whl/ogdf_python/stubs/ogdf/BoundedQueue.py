# file stubs/ogdf/BoundedQueue.py generated from classogdf_1_1_bounded_queue
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
INDEX = TypeVar('INDEX')

E = TypeVar('E')

class BoundedQueue(Generic[E, INDEX]):

	"""The parameterized classBoundedQueueimplements queues with bounded size."""

	@overload
	def __init__(self) -> None:
		"""Pointer to first element of total array."""
		...

	@overload
	def __init__(self, Q : BoundedQueue[ E ]) -> None:
		"""Constructs a bounded queue containing the elements ofQ(move semantics)."""
		...

	@overload
	def __init__(self, Q : BoundedQueue[ E ]) -> None:
		"""Constructs a bounded queue that is a copy ofQ."""
		...

	@overload
	def __init__(self, n : INDEX) -> None:
		"""Constructs an empty bounded queue for at mostnelements."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def append(self, x : E) -> None:
		"""Addsxat the end of queue."""
		...

	@overload
	def bottom(self) -> E:
		"""Returns back element."""
		...

	@overload
	def bottom(self) -> E:
		"""Returns back element."""
		...

	def capacity(self) -> INDEX:
		"""Returns the capacity of the bounded queue."""
		...

	def clear(self) -> None:
		"""Makes the queue empty."""
		...

	def empty(self) -> bool:
		"""Returns true iff the queue is empty."""
		...

	def full(self) -> bool:
		"""Returns true iff the queue is full."""
		...

	@overload
	def init(self) -> None:
		"""Reinitializes the bounded queue to a non-valid bounded queue."""
		...

	@overload
	def init(self, n : INDEX) -> None:
		"""Reinitializes the bounded queue to a bounded queue for at mostnelements."""
		...

	@overload
	def __assign__(self, Q : BoundedQueue[ E ]) -> BoundedQueue[ E ]:
		"""Assignment operator (move semantics)."""
		...

	@overload
	def __assign__(self, Q : BoundedQueue[ E ]) -> BoundedQueue[ E ]:
		"""Assignment operator."""
		...

	def pop(self) -> E:
		"""Removes front element and returns it."""
		...

	def print(self, os : std.ostream, delim : int = ' ') -> None:
		"""Prints the queue to output streamoswith the seperatordelim."""
		...

	def size(self) -> INDEX:
		"""Returns current size of the queue."""
		...

	@overload
	def top(self) -> E:
		"""Returns front element."""
		...

	@overload
	def top(self) -> E:
		"""Returns front element."""
		...
