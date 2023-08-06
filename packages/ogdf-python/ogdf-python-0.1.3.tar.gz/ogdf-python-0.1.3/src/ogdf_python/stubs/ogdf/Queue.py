# file stubs/ogdf/Queue.py generated from classogdf_1_1_queue
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Args = TypeVar('Args')

E = TypeVar('E')

class Queue(ogdf.SList[ E ], Generic[E]):

	"""The parameterized class Queue<E> implements list-based queues."""

	# Access methods

	def empty(self) -> bool:
		"""Returns true iff the queue is empty."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the queue."""
		...

	@overload
	def top(self) -> const_reference:
		"""Returns a reference to the front element."""
		...

	@overload
	def top(self) -> reference:
		"""Returns a reference to the front element."""
		...

	@overload
	def bottom(self) -> const_reference:
		"""Returns a reference to the back element."""
		...

	@overload
	def bottom(self) -> reference:
		"""Returns a reference to the back element."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first element of the queue."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first element of the queue."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first element of the queue."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last element of the queue."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last element of the queue."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last element of the queue."""
		...

	@overload
	def backIterator(self) -> iterator:
		"""Returns an iterator to the last element of the queue."""
		...

	@overload
	def backIterator(self) -> const_iterator:
		"""Returns a const iterator to the last element of the queue."""
		...

	# Operators

	@overload
	def __assign__(self, Q : Queue[ E ]) -> Queue[ E ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, Q : Queue[ E ]) -> Queue[ E ]:
		"""Assignment operator (move semantics)."""
		...

	def getList(self) -> SList[ E ]:
		"""Conversion to constSList."""
		...

	# Adding and removing elements

	def append(self, x : E) -> iterator:
		"""Addsxat the end of queue."""
		...

	def emplace(self, args : Args) -> iterator:
		"""Adds a new element at the end of the queue."""
		...

	def pop(self) -> E:
		"""Removes front element and returns it."""
		...

	def clear(self) -> None:
		"""Makes the queue empty."""
		...

	#: Provides a forward iterator that can read a const element in a queue.
	const_iterator : Type = SListConstIterator[ E ]

	#: Provides a reference to a const element stored in a queue for reading and performing const operations.
	const_reference : Type = E

	#: Provides a forward iterator that can read or modify any element in a queue.
	iterator : Type = SListIterator[ E ]

	#: Provides a reference to an element stored in a queue.
	reference : Type = E

	#: Represents the data type stored in a queue element.
	value_type : Type = E

	@overload
	def __init__(self) -> None:
		"""Constructs an empty queue."""
		...

	@overload
	def __init__(self, Q : Queue[ E ]) -> None:
		"""Constructs a queue that is a copy ofQ."""
		...

	@overload
	def __init__(self, Q : Queue[ E ]) -> None:
		"""Constructs a queue containing the elements ofQ(move semantics)."""
		...

	@overload
	def __init__(self, initList : std.initializer_list[ E ]) -> None:
		"""Constructs a queue and appends the elements ininitListto it."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...
