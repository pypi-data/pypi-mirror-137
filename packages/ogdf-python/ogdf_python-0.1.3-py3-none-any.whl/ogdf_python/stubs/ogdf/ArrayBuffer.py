# file stubs/ogdf/ArrayBuffer.py generated from classogdf_1_1_array_buffer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
# std::enable_if<!OGDF_TRIVIALLY_COPYABLE< EE >::value, int >::type

EE = TypeVar('EE')

INDEX = TypeVar('INDEX')

# std::enable_if< OGDF_TRIVIALLY_COPYABLE< EE >::value, int >::type

COMPARER = TypeVar('COMPARER')

RNG = TypeVar('RNG')

E = TypeVar('E')

class ArrayBuffer(Generic[E, INDEX]):

	"""An array that keeps track of the number of inserted elements; also usable as an efficient stack."""

	# Reordering

	@overload
	def permute(self, l : INDEX, r : INDEX, rng : RNG) -> None:
		"""Randomly permutes the subarray with index set [l..r] using random number generatorrng."""
		...

	@overload
	def permute(self, rng : RNG) -> None:
		"""Randomly permutes the array using random number generatorrng."""
		...

	@overload
	def permute(self, l : INDEX, r : INDEX) -> None:
		"""Randomly permutes the subarray with index set [l..r]."""
		...

	@overload
	def permute(self) -> None:
		"""Randomly permutes the array."""
		...

	const_iterator : Type = Array[ E, INDEX ].const_iterator

	const_reverse_iterator : Type = Array[ E, INDEX ].const_reverse_iterator

	iterator : Type = Array[ E, INDEX ].iterator

	key_type : Type = INDEX

	reverse_iterator : Type = Array[ E, INDEX ].reverse_iterator

	value_type : Type = E

	@overload
	def __init__(self) -> None:
		"""Creates an empty array buffer, without initial memory allocation."""
		...

	@overload
	def __init__(self, buffer : ArrayBuffer[ E, INDEX ]) -> None:
		"""Creates an array buffer containing the elements ofbuffer(move semantics)."""
		...

	@overload
	def __init__(self, source : Array[ E, INDEX ], autogrow : bool = True) -> None:
		"""Creates an array buffer, initialized by the given array; you may specify that the array should not grow."""
		...

	@overload
	def __init__(self, buffer : ArrayBuffer[ E, INDEX ]) -> None:
		"""Creates an array buffer that is a copy ofbuffer."""
		...

	@overload
	def __init__(self, size : INDEX, autogrow : bool = True) -> None:
		"""Creates an empty array buffer, allocating memory for up tosizeelements; you may specify that the array should not grow automatically."""
		...

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first element."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first element."""
		...

	@overload
	def binarySearch(self, e : E) -> INDEX:
		"""Performs a binary search for elemente."""
		...

	@overload
	def binarySearch(self, e : E, comp : COMPARER) -> INDEX:
		"""Performs a binary search for elementewith comparercomp."""
		...

	def capacity(self) -> INDEX:
		"""Returns the current capacity of the datastructure. Note that this value is rather irrelevant if the array is growable."""
		...

	def clear(self) -> None:
		"""Clears the buffer."""
		...

	@overload
	def compactCopy(self, A2 : Array[ E, INDEX ]) -> None:
		"""Generates a compact copy holding the current elements."""
		...

	@overload
	def compactCopy(self, A2 : Array[ E, INDEX ]) -> None:
		"""Generates a compact copy holding the current elements."""
		...

	def compactCpycon(self, A2 : Array[ E, INDEX ]) -> None:
		"""Generates a compact copy holding the current elements."""
		...

	def empty(self) -> bool:
		"""Returns true if the buffer is empty, false otherwise."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one past the last element."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one past the last element."""
		...

	def full(self) -> bool:
		"""Returns true iff the buffer is non-growable and filled."""
		...

	@overload
	def init(self) -> None:
		"""Reinitializes the array, clearing it, and without initial memory allocation."""
		...

	@overload
	def init(self, size : INDEX) -> None:
		"""Reinitializes the array, clearing it, and allocating memory for up tosizeelements."""
		...

	def isGrowable(self) -> bool:
		"""Returns whether the buffer will automatically expand if the initial size is insufficient."""
		...

	def leftShift(self, ind : ArrayBuffer[ INDEX, INDEX ]) -> None:
		"""Removes the components listed in the bufferindby shifting the remaining components to the left."""
		...

	@overload
	def linearSearch(self, x : E) -> INDEX:
		"""Performs a linear search for elementx."""
		...

	@overload
	def linearSearch(self, x : E, comp : COMPARER) -> INDEX:
		"""Performs a linear search for elementxwith comparercomp."""
		...

	def __ne__(self, L : ArrayBuffer[ E, INDEX ]) -> bool:
		"""Inequality operator."""
		...

	@overload
	def __assign__(self, buffer : ArrayBuffer[ E, INDEX ]) -> ArrayBuffer[ E, INDEX ]:
		"""Assignment operator (move semantics)."""
		...

	@overload
	def __assign__(self, buffer : ArrayBuffer[ E, INDEX ]) -> ArrayBuffer[ E, INDEX ]:
		"""Assignment operator."""
		...

	def __eq__(self, L : ArrayBuffer[ E, INDEX ]) -> bool:
		"""Equality operator."""
		...

	@overload
	def __getitem__(self, i : INDEX) -> E:
		"""Returns a reference to the element at positioni."""
		...

	@overload
	def __getitem__(self, i : INDEX) -> E:
		"""Returns a reference to the element at positioni."""
		...

	def pop(self) -> None:
		"""Removes the newest element from the buffer."""
		...

	def popRet(self) -> E:
		"""Removes the newest element from the buffer and returns it."""
		...

	def push(self, e : E) -> None:
		"""Puts a new element in the buffer."""
		...

	@overload
	def quicksort(self) -> None:
		"""Sorts buffer using Quicksort."""
		...

	@overload
	def quicksort(self, comp : COMPARER) -> None:
		"""Sorts buffer using Quicksort and a user-defined comparercomp."""
		...

	@overload
	def rbegin(self) -> reverse_iterator:
		"""Returns a reverse iterator to the last element."""
		...

	@overload
	def rbegin(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to the last element."""
		...

	@overload
	def rend(self) -> reverse_iterator:
		"""Returns a reverse iterator to one before the first element."""
		...

	@overload
	def rend(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to one before the first element."""
		...

	def setCapacity(self, newCapacity : INDEX) -> None:
		"""Changes the capacity of the buffer (independent whether the buffer is growable of not)."""
		...

	def setGrowable(self, _growable : bool) -> None:
		"""Sets the flag whether the buffer will automatically expand if the initial size is insufficient."""
		...

	def size(self) -> INDEX:
		"""Returns number of elements in the buffer."""
		...

	@overload
	def top(self) -> E:
		"""Returns the newest element of the buffer."""
		...

	@overload
	def top(self) -> E:
		"""Returns the newest element of the buffer."""
		...
