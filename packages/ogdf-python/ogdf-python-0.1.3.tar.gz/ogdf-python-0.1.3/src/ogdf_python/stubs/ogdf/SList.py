# file stubs/ogdf/SList.py generated from classogdf_1_1_s_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Args = TypeVar('Args')

E = TypeVar('E')

class SList(ogdf.SListPure[ E ], Generic[E]):

	"""Singly linked lists (maintaining the length of the list)."""

	# Access methods

	def size(self) -> int:
		"""Returns the number of elements in the list."""
		...

	def getSListPure(self) -> SListPure[ E ]:
		"""Conversion to constSListPure."""
		...

	# Operators

	@overload
	def __assign__(self, L : SList[ E ]) -> SList[ E ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, L : SList[ E ]) -> SList[ E ]:
		"""Assignment operator (move semantics)."""
		...

	def __eq__(self, L : SList[ E ]) -> bool:
		"""Equality operator."""
		...

	def __ne__(self, L : SList[ E ]) -> bool:
		"""Inequality operator."""
		...

	# Adding elements

	def pushFront(self, x : E) -> SListIterator[ E ]:
		"""Adds elementxat the beginning of the list."""
		...

	def emplaceFront(self, args : Args) -> iterator:
		"""Adds a new element at the beginning of the list."""
		...

	def pushBack(self, x : E) -> SListIterator[ E ]:
		"""Adds elementxat the end of the list."""
		...

	def emplaceBack(self, args : Args) -> iterator:
		"""Adds a new element at the end of the list."""
		...

	def insertAfter(self, x : E, itBefore : SListIterator[ E ]) -> SListIterator[ E ]:
		"""Inserts elementxafteritBefore."""
		...

	# Removing elements

	def popFront(self) -> None:
		"""Removes the first element from the list."""
		...

	def popFrontRet(self) -> E:
		"""Removes the first element from the list and returns it."""
		...

	def delSucc(self, itBefore : SListIterator[ E ]) -> None:
		"""Removes the succesor ofitBefore."""
		...

	def clear(self) -> None:
		"""Removes all elements from the list."""
		...

	# Moving elements

	def moveFrontToFront(self, L2 : SList[ E ]) -> None:
		"""Moves the first element of this list to the begin of listL2."""
		...

	def moveFrontToBack(self, L2 : SList[ E ]) -> None:
		"""Moves the first element of this list to the end of listL2."""
		...

	def moveFrontToSucc(self, L2 : SList[ E ], itBefore : SListIterator[ E ]) -> None:
		"""Moves the first element of this list to listL2inserted afteritBefore."""
		...

	def conc(self, L2 : SList[ E ]) -> None:
		"""AppendsL2to this list and makesL2empty."""
		...

	@overload
	def __init__(self) -> None:
		"""Constructs an empty singly linked list."""
		...

	@overload
	def __init__(self, L : SList[ E ]) -> None:
		"""Constructs a singly linked list that is a copy ofL."""
		...

	@overload
	def __init__(self, L : SList[ E ]) -> None:
		"""Constructs a singly linked list containing the elements ofL(move semantics)."""
		...

	@overload
	def __init__(self, init : std.initializer_list[ E ]) -> None:
		"""Constructs a singly linked list containing the elements ininit."""
		...
