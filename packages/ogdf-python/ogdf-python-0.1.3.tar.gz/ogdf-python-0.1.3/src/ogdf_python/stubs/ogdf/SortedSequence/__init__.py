# file stubs/ogdf/SortedSequence/__init__.py generated from classogdf_1_1_sorted_sequence
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
INFO = TypeVar('INFO')

KEY = TypeVar('KEY')

CMP = TypeVar('CMP')

class SortedSequence(Generic[KEY, INFO, CMP]):

	"""Maintains a sequence of (key,info) pairs sorted by key."""

	# General information and standard iterators

	def size(self) -> int:
		"""Returns the current size of the sequence, i.e., the number of stored elements."""
		...

	def empty(self) -> bool:
		"""Returns true if the sequence is empty, false otherwise."""
		...

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator pointing to the first element."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const-iterator pointing to the first element."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const-iterator pointing to the first element."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator pointing to one past the last element."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const-iterator pointing to one past the last element."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const-iterator pointing to one past the last element."""
		...

	@overload
	def rbegin(self) -> reverse_iterator:
		"""Returns a reverse iterator pointing to the last element."""
		...

	@overload
	def rbegin(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator pointing to the last element."""
		...

	def crbegin(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator pointing to the last element."""
		...

	@overload
	def rend(self) -> reverse_iterator:
		"""Returns a reverse iterator pointing to one before the first element."""
		...

	@overload
	def rend(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator pointing to one before the first element."""
		...

	def crend(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator pointing to one before the first element."""
		...

	# Lookup operations

	@overload
	def lookup(self, key : KEY) -> iterator:
		"""Returns an iterator to the element with keykey, or a null iterator if no such element exists."""
		...

	@overload
	def lookup(self, key : KEY) -> const_iterator:
		"""Returns a const-iterator to the element with keykey, or a null iterator if no such element exists."""
		...

	@overload
	def locate(self, key : KEY) -> iterator:
		"""Returns an iterator to the element <k1,i1> such thatk1is minimal withk1key, or a null iterator if no such element exists."""
		...

	@overload
	def locate(self, key : KEY) -> const_iterator:
		"""Returns a const-iterator to the element <k1,i1> such thatk1is minimal withk1key, or a null iterator if no such element exists."""
		...

	@overload
	def minItem(self) -> iterator:
		"""Returns an iterator to the element with minimal key if the sequence is not empty, an invalid iterator otherwise."""
		...

	@overload
	def minItem(self) -> const_iterator:
		"""Returns a const-iterator to the element with minimal key if the sequence is not empty, an invalid const-iterator otherwise."""
		...

	@overload
	def maxItem(self) -> reverse_iterator:
		"""Returns a reverse iterator to the element with maximal key if the sequence is not empty, an invalid reverse iterator otherwise."""
		...

	@overload
	def maxItem(self) -> const_reverse_iterator:
		"""Returns a const reverse iterator to the element with maximal key if the sequence is not empty, an invalid const reverse iterator otherwise."""
		...

	# Insertion and deletion

	def insert(self, key : KEY, info : INFO) -> iterator:
		"""Updates information forkeyif contained in sequence, or adds a new element <key,info>."""
		...

	def _del(self, key : KEY) -> None:
		"""Removes the element with keykey(if such an element exists)."""
		...

	def delItem(self, it : iterator) -> None:
		"""Removes the element to whichitpoints from the sequence."""
		...

	def clear(self) -> None:
		"""Removes all elements from the sorted sequence."""
		...

	# Operators

	@overload
	def __assign__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> SortedSequence[ KEY, INFO, CMP ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> SortedSequence[ KEY, INFO, CMP ]:
		"""Assignment operator (move semantics)."""
		...

	def __eq__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> bool:
		"""Returns true if the keys stored in this sequence equal the keys inS, false otherwise."""
		...

	def __ne__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> bool:
		"""Returns false if the keys stored in this sequence equal the keys inS, true otherwise."""
		...

	# Special modification methods

	def insertAfter(self, it : iterator, key : KEY, info : INFO) -> iterator:
		"""Adds a new element <key,info>after elementit."""
		...

	def reverseItems(self, itBegin : iterator, itEnd : iterator) -> None:
		"""Reverses the items in the subsequence fromitBegintoitEnd(inclusive)."""
		...

	#: The const-iterator type for sorted sequences (bidirectional iterator).
	const_iterator : Type = SortedSequenceConstIterator[ KEY, INFO, CMP ]

	#: The const reverse iterator type for sorted sequences (bidirectional iterator).
	const_reverse_iterator : Type = SortedSequenceConstReverseIterator[ KEY, INFO, CMP ]

	#: The iterator type for sorted sequences (bidirectional iterator).
	iterator : Type = SortedSequenceIterator[ KEY, INFO, CMP ]

	#: The reverse iterator type for sorted sequences (bidirectional iterator).
	reverse_iterator : Type = SortedSequenceReverseIterator[ KEY, INFO, CMP ]

	@overload
	def __init__(self, comparer : CMP = CMP()) -> None:
		"""Constructs an initially empty sorted sequence."""
		...

	@overload
	def __init__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, S : SortedSequence[ KEY, INFO, CMP ]) -> None:
		"""Copy constructor (move semantics)."""
		...

	@overload
	def __init__(self, initList : std.initializer_list[ std.pair[ KEY, INFO ]]) -> None:
		"""Constructs a sorted sequence containing the elements ininitList."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...
