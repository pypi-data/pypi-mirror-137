# file stubs/ogdf/SListPure.py generated from classogdf_1_1_s_list_pure
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Args = TypeVar('Args')

COMPARER = TypeVar('COMPARER')

E = TypeVar('E')

RNG = TypeVar('RNG')

class SListPure(Generic[E]):

	"""Singly linked lists."""

	# Access methods

	def empty(self) -> bool:
		"""Returns true iff the list is empty."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the list."""
		...

	@overload
	def front(self) -> const_reference:
		"""Returns a reference to the first element."""
		...

	@overload
	def front(self) -> reference:
		"""Returns a reference to the first element."""
		...

	@overload
	def back(self) -> const_reference:
		"""Returns a reference to the last element."""
		...

	@overload
	def back(self) -> reference:
		"""Returns a reference to the last element."""
		...

	@overload
	def get(self, pos : int) -> const_iterator:
		"""Returns an iterator pointing to the element at positionpos."""
		...

	@overload
	def get(self, pos : int) -> iterator:
		"""Returns an iterator pointing to the element at positionpos."""
		...

	def pos(self, it : const_iterator) -> int:
		"""Returns the position (starting with 0) ofitin the list."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first element of the list."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first element of the list."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first element of the list."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last element of the list."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last element of the list."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last element of the list."""
		...

	@overload
	def backIterator(self) -> iterator:
		"""Returns an iterator to the last element of the list."""
		...

	@overload
	def backIterator(self) -> const_iterator:
		"""Returns a const iterator to the last element of the list."""
		...

	@overload
	def cyclicSucc(self, it : const_iterator) -> const_iterator:
		"""Returns an iterator to the cyclic successor ofit."""
		...

	@overload
	def cyclicSucc(self, it : iterator) -> iterator:
		"""Returns an iterator to the cyclic successor ofit."""
		...

	# Operators

	@overload
	def __assign__(self, L : SListPure[ E ]) -> SListPure[ E ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, L : SListPure[ E ]) -> SListPure[ E ]:
		"""Assignment operator (move semantics)."""
		...

	def __eq__(self, L : SListPure[ E ]) -> bool:
		"""Equality operator."""
		...

	def __ne__(self, L : SListPure[ E ]) -> bool:
		"""Inequality operator."""
		...

	# Adding elements

	def pushFront(self, x : E) -> iterator:
		"""Adds elementxat the beginning of the list."""
		...

	def emplaceFront(self, args : Args) -> iterator:
		"""Adds a new element at the beginning of the list."""
		...

	def pushBack(self, x : E) -> iterator:
		"""Adds elementxat the end of the list."""
		...

	def emplaceBack(self, args : Args) -> iterator:
		"""Adds a new element at the end of the list."""
		...

	def insertAfter(self, x : E, itBefore : iterator) -> iterator:
		"""Inserts elementxafteritBefore."""
		...

	# Removing elements

	def popFront(self) -> None:
		"""Removes the first element from the list."""
		...

	def popFrontRet(self) -> E:
		"""Removes the first element from the list and returns it."""
		...

	def delSucc(self, itBefore : iterator) -> None:
		"""Removes the succesor ofitBefore."""
		...

	def clear(self) -> None:
		"""Removes all elements from the list."""
		...

	# Moving elements

	def moveFrontToFront(self, L2 : SListPure[ E ]) -> None:
		"""Moves the first element of this list to the begin of listL2."""
		...

	def moveFrontToBack(self, L2 : SListPure[ E ]) -> None:
		"""Moves the first element of this list to the end of listL2."""
		...

	def moveFrontToSucc(self, L2 : SListPure[ E ], itBefore : iterator) -> None:
		"""Moves the first element of this list to listL2inserted afteritBefore."""
		...

	def conc(self, L2 : SListPure[ E ]) -> None:
		"""AppendsL2to this list and makesL2empty."""
		...

	def reverse(self) -> None:
		"""Reverses the order of the list elements."""
		...

	# Searching and sorting

	@overload
	def search(self, e : E) -> SListConstIterator[ E ]:
		"""Scans the list for the specified element and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E) -> SListIterator[ E ]:
		"""Scans the list for the specified element and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E, comp : COMPARER) -> SListConstIterator[ E ]:
		"""Scans the list for the specified element (using the user-defined comparer) and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E, comp : COMPARER) -> SListIterator[ E ]:
		"""Scans the list for the specified element (using the user-defined comparer) and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def quicksort(self) -> None:
		"""Sorts the list using Quicksort."""
		...

	@overload
	def quicksort(self, comp : COMPARER) -> None:
		"""Sorts the list using Quicksort and comparercomp."""
		...

	@overload
	def bucketSort(self, l : int, h : int, f : BucketFunc[ E ]) -> None:
		"""Sorts the list using bucket sort."""
		...

	@overload
	def bucketSort(self, f : BucketFunc[ E ]) -> None:
		"""Sorts the list using bucket sort."""
		...

	# Random elements and permutations

	@overload
	def chooseIterator(self, includeElement : Callable = print, isFastTest : bool = True) -> const_iterator:
		...

	@overload
	def chooseIterator(self, includeElement : Callable = print, isFastTest : bool = True) -> iterator:
		...

	@overload
	def chooseElement(self, includeElement : Callable = print, isFastTest : bool = True) -> const_reference:
		...

	@overload
	def chooseElement(self, includeElement : Callable = print, isFastTest : bool = True) -> reference:
		...

	@overload
	def permute(self) -> None:
		"""Randomly permutes the elements in the list."""
		...

	@overload
	def permute(self, rng : RNG) -> None:
		"""Randomly permutes the elements in the list using random number generatorrng."""
		...

	def copy(self, L : SListPure[ E ]) -> None:
		...

	@overload
	def permute(self, n : int, rng : RNG) -> None:
		"""Permutes elements in list randomly;nis the length of the list."""
		...

	def reassignListRefs(self, start : SListElement[ E ] = None) -> None:
		"""Sets the debug reference of all list elements starting atstarttothis."""
		...

	#: Provides a forward iterator that can read a const element in a list.
	const_iterator : Type = SListConstIterator[ E ]

	#: Provides a reference to a const element stored in a list for reading and performing const operations.
	const_reference : Type = E

	#: Provides a forward iterator that can read or modify any element in a list.
	iterator : Type = SListIterator[ E ]

	#: Provides a reference to an element stored in a list.
	reference : Type = E

	#: Represents the data type stored in a list element.
	value_type : Type = E

	@overload
	def __init__(self) -> None:
		"""Constructs an empty singly linked list."""
		...

	@overload
	def __init__(self, L : SListPure[ E ]) -> None:
		"""Constructs a singly linked list that is a copy ofL."""
		...

	@overload
	def __init__(self, L : SListPure[ E ]) -> None:
		"""Constructs a singly linked list containing the elements ofL(move semantics)."""
		...

	@overload
	def __init__(self, init : std.initializer_list[ E ]) -> None:
		"""Constructs a singly linked list containing the elements ininit."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...
