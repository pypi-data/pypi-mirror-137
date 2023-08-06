# file stubs/ogdf/ListPure.py generated from classogdf_1_1_list_pure
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Args = TypeVar('Args')

COMPARER = TypeVar('COMPARER')

E = TypeVar('E')

RNG = TypeVar('RNG')

class ListPure(Generic[E]):

	"""Doubly linked lists."""

	# Access methods

	def empty(self) -> bool:
		"""Returns true iff the list is empty."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the list."""
		...

	@overload
	def front(self) -> const_reference:
		"""Returns a const reference to the first element."""
		...

	@overload
	def front(self) -> reference:
		"""Returns a reference to the first element."""
		...

	@overload
	def back(self) -> const_reference:
		"""Returns a const reference to the last element."""
		...

	@overload
	def back(self) -> reference:
		"""Returns a reference to the last element."""
		...

	@overload
	def get(self, pos : int) -> const_iterator:
		"""Returns a const iterator pointing to the element at positionpos."""
		...

	@overload
	def get(self, pos : int) -> iterator:
		"""Returns an iterator pointing to the element at positionpos."""
		...

	def pos(self, it : const_iterator) -> int:
		"""Returns the position (starting with 0) of iteratoritin the list."""
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
	def rbegin(self) -> reverse_iterator:
		"""Returns an iterator to the last element of the list."""
		...

	@overload
	def rbegin(self) -> const_reverse_iterator:
		"""Returns a const iterator to the last element of the list."""
		...

	def crbegin(self) -> const_reverse_iterator:
		"""Returns a const iterator to the last element of the list."""
		...

	@overload
	def rend(self) -> reverse_iterator:
		"""Returns an iterator to one-before-first element of the list."""
		...

	@overload
	def rend(self) -> const_reverse_iterator:
		"""Returns a const iterator to one-before-first element of the list."""
		...

	def crend(self) -> const_reverse_iterator:
		"""Returns a const iterator to one-before-first element of the list."""
		...

	@overload
	def cyclicSucc(self, it : const_iterator) -> const_iterator:
		"""Returns a const iterator to the cyclic successor ofit."""
		...

	@overload
	def cyclicSucc(self, it : iterator) -> iterator:
		"""Returns an iterator to the cyclic successor ofit."""
		...

	@overload
	def cyclicSucc(self, it : const_reverse_iterator) -> const_reverse_iterator:
		...

	@overload
	def cyclicSucc(self, it : reverse_iterator) -> reverse_iterator:
		...

	@overload
	def cyclicPred(self, it : const_iterator) -> const_iterator:
		"""Returns a const iterator to the cyclic predecessor ofit."""
		...

	@overload
	def cyclicPred(self, it : iterator) -> iterator:
		"""Returns an iterator to the cyclic predecessor ofit."""
		...

	@overload
	def cyclicPred(self, it : const_reverse_iterator) -> const_reverse_iterator:
		...

	@overload
	def cyclicPred(self, it : reverse_iterator) -> reverse_iterator:
		...

	# Operators

	@overload
	def __assign__(self, L : ListPure[ E ]) -> ListPure[ E ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, L : ListPure[ E ]) -> ListPure[ E ]:
		"""Assignment operator (move semantics)."""
		...

	def __eq__(self, L : ListPure[ E ]) -> bool:
		"""Equality operator."""
		...

	def __ne__(self, L : ListPure[ E ]) -> bool:
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

	def insert(self, x : E, it : iterator, dir : Direction = Direction.after) -> iterator:
		"""Inserts elementxbefore or afterit."""
		...

	def insertBefore(self, x : E, it : iterator) -> iterator:
		"""Inserts elementxbeforeit."""
		...

	def insertAfter(self, x : E, it : iterator) -> iterator:
		"""Inserts elementxafterit."""
		...

	# Removing elements

	def popFront(self) -> None:
		"""Removes the first element from the list."""
		...

	def popFrontRet(self) -> E:
		"""Removes the first element from the list and returns it."""
		...

	def popBack(self) -> None:
		"""Removes the last element from the list."""
		...

	def popBackRet(self) -> E:
		"""Removes the last element from the list and returns it."""
		...

	def _del(self, it : iterator) -> None:
		"""Removesitfrom the list."""
		...

	def removeFirst(self, x : E) -> bool:
		"""Removes the first occurrence ofx(if any) from the list."""
		...

	def clear(self) -> None:
		"""Removes all elements from the list."""
		...

	# Moving elements

	def exchange(self, it1 : iterator, it2 : iterator) -> None:
		"""Exchanges the positions ofit1andit2in the list."""
		...

	@overload
	def moveToFront(self, it : iterator) -> None:
		"""Movesitto the begin of the list."""
		...

	@overload
	def moveToBack(self, it : iterator) -> None:
		"""Movesitto the end of the list."""
		...

	@overload
	def moveToSucc(self, it : iterator, itBefore : iterator) -> None:
		"""MovesitafteritBefore."""
		...

	@overload
	def moveToPrec(self, it : iterator, itAfter : iterator) -> None:
		"""MovesitbeforeitAfter."""
		...

	@overload
	def moveToFront(self, it : iterator, L2 : ListPure[ E ]) -> None:
		"""Movesitto the begin ofL2."""
		...

	@overload
	def moveToBack(self, it : iterator, L2 : ListPure[ E ]) -> None:
		"""Movesitto the end ofL2."""
		...

	@overload
	def moveToSucc(self, it : iterator, L2 : ListPure[ E ], itBefore : iterator) -> None:
		"""Movesitto listL2and inserts it afteritBefore."""
		...

	@overload
	def moveToPrec(self, it : iterator, L2 : ListPure[ E ], itAfter : iterator) -> None:
		"""Movesitto listL2and inserts it beforeitAfter."""
		...

	def conc(self, L2 : ListPure[ E ]) -> None:
		"""AppendsL2to this list and makesL2empty."""
		...

	def concFront(self, L2 : ListPure[ E ]) -> None:
		"""PrependsL2to this list and makesL2empty."""
		...

	def swap(self, other : ListPure[ E ]) -> None:
		"""Exchanges the contents of this list andotherin constant time."""
		...

	def split(self, it : iterator, L1 : ListPure[ E ], L2 : ListPure[ E ], dir : Direction = Direction.before) -> None:
		"""Splits the list at elementitinto listsL1andL2."""
		...

	def splitAfter(self, it : iterator, L2 : ListPure[ E ]) -> None:
		"""Splits the list afterit."""
		...

	def splitBefore(self, it : iterator, L2 : ListPure[ E ]) -> None:
		"""Splits the list beforeit."""
		...

	def reverse(self) -> None:
		"""Reverses the order of the list elements."""
		...

	# Searching and sorting

	@overload
	def search(self, e : E) -> ListConstIterator[ E ]:
		"""Scans the list for the specified element and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E) -> ListIterator[ E ]:
		"""Scans the list for the specified element and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E, comp : COMPARER) -> ListConstIterator[ E ]:
		"""Scans the list for the specified element (using the user-defined comparer) and returns an iterator to the first occurrence in the list, or an invalid iterator if not found."""
		...

	@overload
	def search(self, e : E, comp : COMPARER) -> ListIterator[ E ]:
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

	def bucketSort(self, l : int, h : int, f : BucketFunc[ E ]) -> None:
		"""Sorts the list using bucket sort."""
		...

	# Random elements and permutations

	@overload
	def chooseIterator(self, includeElement : Callable = print, isFastTest : bool = True) -> const_iterator:
		"""Returns an iterator to a random element."""
		...

	@overload
	def chooseIterator(self, includeElement : Callable = print, isFastTest : bool = True) -> iterator:
		"""Returns an iterator to a random element."""
		...

	@overload
	def chooseElement(self, includeElement : Callable = print, isFastTest : bool = True) -> const_reference:
		"""Returns a random element."""
		...

	@overload
	def chooseElement(self, includeElement : Callable = print, isFastTest : bool = True) -> reference:
		"""Returns a random element."""
		...

	@overload
	def permute(self) -> None:
		"""Randomly permutes the elements in the list."""
		...

	@overload
	def permute(self, rng : RNG) -> None:
		"""Randomly permutes the elements in the list using random number generatorrng."""
		...

	def copy(self, L : ListPure[ E ]) -> None:
		...

	@overload
	def permute(self, n : int, rng : RNG) -> None:
		"""permutes elements in list randomly; n is the length of the list"""
		...

	def reassignListRefs(self, start : ListElement[ E ] = None) -> None:
		"""Sets the debug reference of all list elements starting atstarttothis."""
		...

	#: Provides a bidirectional iterator that can read a const element in a list.
	const_iterator : Type = ListConstIterator[ E ]

	#: Provides a reference to a const element stored in a list for reading and performing const operations.
	const_reference : Type = E

	#: Provides a bidirectional reverse iterator that can read a const element in a list.
	const_reverse_iterator : Type = ListConstReverseIterator[ E ]

	#: Provides a bidirectional iterator that can read or modify any element in a list.
	iterator : Type = ListIterator[ E ]

	#: Provides a reference to an element stored in a list.
	reference : Type = E

	#: Provides a bidirectional reverse iterator that can read or modify any element in a list.
	reverse_iterator : Type = ListReverseIterator[ E ]

	#: Represents the data type stored in a list element.
	value_type : Type = E

	#: Pointer to first element.
	m_head : ListElement[ E ] = ...

	#: Pointer to last element.
	m_tail : ListElement[ E ] = ...

	@overload
	def __init__(self) -> None:
		"""Constructs an empty doubly linked list."""
		...

	@overload
	def __init__(self, L : ListPure[ E ]) -> None:
		"""Constructs a doubly linked list that is a copy ofL."""
		...

	@overload
	def __init__(self, L : ListPure[ E ]) -> None:
		"""Constructs a doubly linked list containing the elements ofL(move semantics)."""
		...

	@overload
	def __init__(self, init : std.initializer_list[ E ]) -> None:
		"""Constructs a doubly linked list containing the elements ininit."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...
