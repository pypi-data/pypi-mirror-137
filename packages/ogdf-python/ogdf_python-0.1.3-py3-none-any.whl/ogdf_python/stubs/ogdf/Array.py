# file stubs/ogdf/Array.py generated from classogdf_1_1_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
COMPARER = TypeVar('COMPARER')

INDEX = TypeVar('INDEX')

E = TypeVar('E')

RNG = TypeVar('RNG')

class Array(Generic[E, INDEX]):

	"""The parameterized classArrayimplements dynamic arrays of typeE."""

	# Access methods

	def low(self) -> INDEX:
		"""Returns the minimal array index."""
		...

	def high(self) -> INDEX:
		"""Returns the maximal array index."""
		...

	def size(self) -> INDEX:
		"""Returns the size (number of elements) of the array."""
		...

	def empty(self) -> bool:
		"""Returnstrueiff there are no elements in the array."""
		...

	@overload
	def __getitem__(self, i : INDEX) -> const_reference:
		"""Returns a reference to the element at positioni."""
		...

	@overload
	def __getitem__(self, i : INDEX) -> reference:
		"""Returns a reference to the element at positioni."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first element."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first element."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first element."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one past the last element."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one past the last element."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one past the last element."""
		...

	@overload
	def rbegin(self) -> reverse_iterator:
		"""Returns an reverse iterator to the last element."""
		...

	@overload
	def rbegin(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to the last element."""
		...

	def crbegin(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to the last element."""
		...

	@overload
	def rend(self) -> reverse_iterator:
		"""Returns an reverse iterator to one before the first element."""
		...

	@overload
	def rend(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to one before the first element."""
		...

	def crend(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to one before the first element."""
		...

	# Initialization and assignment

	@overload
	def init(self) -> None:
		"""Reinitializes the array to an array with empty index set."""
		...

	@overload
	def init(self, s : INDEX) -> None:
		"""Reinitializes the array to an array with index set [0..s-1]."""
		...

	@overload
	def init(self, a : INDEX, b : INDEX) -> None:
		"""Reinitializes the array to an array with index set [a..b]."""
		...

	@overload
	def init(self, a : INDEX, b : INDEX, x : E) -> None:
		"""Reinitializes the array to an array with index set [a..b] and sets all entries tox."""
		...

	@overload
	def fill(self, x : E) -> None:
		"""Sets all elements tox."""
		...

	@overload
	def fill(self, i : INDEX, j : INDEX, x : E) -> None:
		"""Sets elements in the intervall [i..j] tox."""
		...

	@overload
	def grow(self, add : INDEX, x : E) -> None:
		"""Enlarges the array byaddelements and sets new elements tox."""
		...

	@overload
	def grow(self, add : INDEX) -> None:
		"""Enlarges the array byaddelements."""
		...

	@overload
	def resize(self, newSize : INDEX, x : E) -> None:
		"""Resizes (enlarges or shrinks) the array to holdnewSizeelements and sets new elements tox."""
		...

	@overload
	def resize(self, newSize : INDEX) -> None:
		"""Resizes (enlarges or shrinks) the array to holdnewSizeelements."""
		...

	@overload
	def __assign__(self, A : Array[ E, INDEX ]) -> Array[ E, INDEX ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, A : Array[ E, INDEX ]) -> Array[ E, INDEX ]:
		"""Assignment operator (move semantics)."""
		...

	# Comparison

	def __eq__(self, L : Array[ E, INDEX ]) -> bool:
		"""Equality operator."""
		...

	def __ne__(self, L : Array[ E, INDEX ]) -> bool:
		"""Inequality operator."""
		...

	# Reordering

	def swap(self, i : INDEX, j : INDEX) -> None:
		"""Swaps the elements at positioniandj."""
		...

	@overload
	def permute(self, l : INDEX, r : INDEX) -> None:
		"""Randomly permutes the subarray with index set [l..r]."""
		...

	@overload
	def permute(self) -> None:
		"""Randomly permutes the array."""
		...

	@overload
	def permute(self, l : INDEX, r : INDEX, rng : RNG) -> None:
		"""Randomly permutes the subarray with index set [l..r] using random number generatorrng."""
		...

	@overload
	def permute(self, rng : RNG) -> None:
		"""Randomly permutes the array using random number generatorrng."""
		...

	# Searching and sorting

	@overload
	def binarySearch(self, e : E) -> int:
		"""Performs a binary search for elemente."""
		...

	@overload
	def binarySearch(self, l : INDEX, r : INDEX, e : E) -> int:
		"""Performs a binary search for elementewithin the array section [l, ...,r] ."""
		...

	@overload
	def binarySearch(self, e : E, comp : COMPARER) -> int:
		"""Performs a binary search for elementewith comparercomp."""
		...

	@overload
	def binarySearch(self, l : INDEX, r : INDEX, e : E, comp : COMPARER) -> INDEX:
		"""Performs a binary search for elementewithin the array section [l, ...,r] with comparercomp."""
		...

	@overload
	def linearSearch(self, e : E) -> INDEX:
		"""Performs a linear search for elemente."""
		...

	@overload
	def linearSearch(self, e : E, comp : COMPARER) -> INDEX:
		"""Performs a linear search for elementewith comparercomp."""
		...

	@overload
	def quicksort(self) -> None:
		"""Sorts array using Quicksort."""
		...

	@overload
	def quicksort(self, l : INDEX, r : INDEX) -> None:
		"""Sorts subarray with index set [l, ...,r] using Quicksort."""
		...

	@overload
	def quicksort(self, comp : COMPARER) -> None:
		"""Sorts array using Quicksort and a user-defined comparercomp."""
		...

	@overload
	def quicksort(self, l : INDEX, r : INDEX, comp : COMPARER) -> None:
		"""Sorts the subarray with index set [l, ...,r] using Quicksort and a user-defined comparercomp."""
		...

	@overload
	def leftShift(self, ind : ArrayBuffer[ INDEX, INDEX ]) -> None:
		"""Removes the components listed inindby shifting the remaining components to the left."""
		...

	@overload
	def leftShift(self, ind : ArrayBuffer[ INDEX, INDEX ], val : E) -> None:
		"""Removes the components listed inindby shifting the remaining components to the left."""
		...

	#: Provides a random-access iterator that can read a const element in an array.
	const_iterator : Type = ArrayConstIterator[ E ]

	#: Provides a reference to a const element stored in an array for reading and performing const operations.
	const_reference : Type = E

	#: Provides a reverse random-access iterator that can read a const element in an array.
	const_reverse_iterator : Type = ArrayConstReverseIterator[ E ]

	#: Provides a random-access iterator that can read or modify any element in an array.
	iterator : Type = ArrayIterator[ E ]

	#: Provides a reference to an element stored in an array.
	reference : Type = E

	#: Provides a reverse random-access iterator that can read or modify any element in an array.
	reverse_iterator : Type = ArrayReverseIterator[ E ]

	#: Represents the data type stored in an array element.
	value_type : Type = E

	#: Threshold used byquicksort()such that insertion sort is called for instances smaller thanmaxSizeInsertionSort.
	maxSizeInsertionSort : int = ...

	@overload
	def __init__(self) -> None:
		"""Creates an array with empty index set."""
		...

	@overload
	def __init__(self, A : Array[ E, INDEX ]) -> None:
		"""Creates an array containing the elements ofA(move semantics)."""
		...

	@overload
	def __init__(self, A : Array[ E, INDEX ]) -> None:
		"""Creates an array that is a copy ofA."""
		...

	@overload
	def __init__(self, A : ArrayBuffer[ E, INDEX ]) -> None:
		"""Creates an array that is a copy ofA. The array-size is set to be the number of elements (not the capacity) of the buffer."""
		...

	@overload
	def __init__(self, a : INDEX, b : INDEX) -> None:
		"""Creates an array with index set [a..b]."""
		...

	@overload
	def __init__(self, a : INDEX, b : INDEX, x : E) -> None:
		"""Creates an array with index set [a..b] and initializes each element withx."""
		...

	@overload
	def __init__(self, s : INDEX) -> None:
		"""Creates an array with index set [0..s-1]."""
		...

	@overload
	def __init__(self, initList : std.initializer_list[ E ]) -> None:
		"""Creates an array containing the elements in the initializer listinitList."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...
