# file stubs/ogdf/List.py generated from classogdf_1_1_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Args = TypeVar('Args')

E = TypeVar('E')

class List(Generic[E]):

	"""Doubly linked lists (maintaining the length of the list)."""

	# Access methods

	def size(self) -> int:
		"""Returns the number of elements in the list."""
		...

	def getListPure(self) -> ListPure[ E ]:
		"""Conversion to constListPure."""
		...

	# Operators

	@overload
	def __assign__(self, L : List[ E ]) -> List[ E ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, L : List[ E ]) -> List[ E ]:
		"""Assignment operator (move semantics)."""
		...

	def __eq__(self, L : List[ E ]) -> bool:
		"""Equality operator."""
		...

	def __ne__(self, L : List[ E ]) -> bool:
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

	def moveToFront(self, it : iterator, L2 : List[ E ]) -> None:
		"""Movesitto the begin of the list."""
		...

	def moveToBack(self, it : iterator, L2 : List[ E ]) -> None:
		"""Movesitto the end of the list."""
		...

	def moveToSucc(self, it : iterator, L2 : List[ E ], itBefore : iterator) -> None:
		"""MovesitafteritBefore."""
		...

	def moveToPrec(self, it : iterator, L2 : List[ E ], itAfter : iterator) -> None:
		"""MovesitbeforeitAfter."""
		...

	def conc(self, L2 : List[ E ]) -> None:
		"""AppendsL2to this list and makesL2empty."""
		...

	def concFront(self, L2 : List[ E ]) -> None:
		"""PrependsL2to this list and makesL2empty."""
		...

	def swap(self, other : List[ E ]) -> None:
		"""Exchanges the contents of this list andotherin constant time."""
		...

	def split(self, it : iterator, L1 : List[ E ], L2 : List[ E ], dir : Direction = Direction.before) -> None:
		"""Splits the list at elementitinto listsL1andL2."""
		...

	@overload
	def __init__(self) -> None:
		"""Constructs an empty doubly linked list."""
		...

	@overload
	def __init__(self, L : List[ E ]) -> None:
		"""Constructs a doubly linked list that is a copy ofL."""
		...

	@overload
	def __init__(self, L : List[ E ]) -> None:
		"""Constructs a doubly linked list containing the elements ofL(move semantics)."""
		...

	@overload
	def __init__(self, init : std.initializer_list[ E ]) -> None:
		"""Constructs a doubly linked list containing the elements ininit."""
		...
