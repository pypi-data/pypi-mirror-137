# file stubs/ogdf/PriorityQueue.py generated from classogdf_1_1_priority_queue
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

Impl = TypeVar('Impl')

T = TypeVar('T')

InputIt = TypeVar('InputIt')

class PriorityQueue(Generic[T, C, Impl]):

	"""Priority queue interface wrapper for heaps."""

	const_reference : Type = value_type

	handle : Type = SpecImpl.Handle

	reference : Type = value_type

	size_type : Type = std.size_t

	value_type : Type = T

	@overload
	def __init__(self, cmp : C = C(), initialSize : int = 128) -> None:
		"""Creates empty priority queue."""
		...

	@overload
	def __init__(self, other : PriorityQueue) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, first : InputIt, last : InputIt, cmp : C = C()) -> None:
		"""Creates priority queue with contents of the given range."""
		...

	@overload
	def __init__(self, other : PriorityQueue) -> None:
		"""Move constructor."""
		...

	@overload
	def __init__(self, init : std.initializer_list[value_type], cmp : C = C()) -> None:
		"""Creates priority queue with contents of the given initializer list."""
		...

	def __destruct__(self) -> None:
		"""Destroys the underlying data structure."""
		...

	def clear(self) -> None:
		"""Removes all the entries from the queue."""
		...

	def decrease(self, pos : handle, value : T) -> None:
		"""Decreases value of the element specified byhandletovalue."""
		...

	def empty(self) -> bool:
		"""Checks whether the queue is empty."""
		...

	def merge(self, other : PriorityQueue) -> None:
		"""Merges in enqueued values ofotherqueue."""
		...

	@overload
	def __assign__(self, other : PriorityQueue) -> PriorityQueue:
		"""Copy and move assignment."""
		...

	@overload
	def __assign__(self, ilist : std.initializer_list[value_type]) -> PriorityQueue:
		"""Assigns the priority queue contents of the given initializer list."""
		...

	def pop(self) -> None:
		"""Removes the top element from the heap."""
		...

	@overload
	def push(self, value : value_type) -> handle:
		"""Inserts a new element with givenvalueinto the queue."""
		...

	@overload
	def push(self, first : InputIt, last : InputIt) -> None:
		"""Inserts new elements specified by the given range."""
		...

	@overload
	def push(self, ilist : std.initializer_list[value_type]) -> None:
		"""Inserts new elements specified by the given initializer list."""
		...

	def size(self) -> size_type:
		"""Returns the number of enqueued elements."""
		...

	def swap(self, other : PriorityQueue) -> None:
		"""Swaps the contents."""
		...

	def top(self) -> T:
		"""Returns reference to the top element in the queue."""
		...

	def value(self, pos : handle) -> T:
		"""Returns the priority of that handle."""
		...
