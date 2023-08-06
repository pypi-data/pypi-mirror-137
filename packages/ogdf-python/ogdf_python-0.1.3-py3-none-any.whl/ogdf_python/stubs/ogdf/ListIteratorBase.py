# file stubs/ogdf/ListIteratorBase.py generated from classogdf_1_1_list_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E = TypeVar('E')

isArgConst = TypeVar('isArgConst')

isArgReverse = TypeVar('isArgReverse')

isReverse = TypeVar('isReverse')

isConst = TypeVar('isConst')

# std::enable_if< isConst||!isArgConst, int >::type

class ListIteratorBase(Generic[E, isConst, isReverse]):

	"""Encapsulates a pointer to a list element."""

	@overload
	def __init__(self) -> None:
		"""Constructs an invalid iterator."""
		...

	@overload
	def __init__(self, it : ListIteratorBase[ E, isArgConst, isArgReverse ]) -> None:
		"""Constructs an iterator that is a copy ofit."""
		...

	@overload
	def __init__(self, it : ListIteratorBase[ E, isConst, isReverse ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, pX : ListElem) -> None:
		"""Constructs an iterator that points topX."""
		...

	def __ne__(self, it : ListIteratorBase[ E, isConst, isReverse ]) -> bool:
		"""Inequality operator."""
		...

	def __deref__(self) -> Elem:
		"""Returns a reference to the element content."""
		...

	def __preinc__(self) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Increment operator (prefix)."""
		...

	def __postinc__(self, _ : int) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Increment operator (postfix)."""
		...

	def __predec__(self) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Decrement operator (prefix)."""
		...

	def __postdec__(self, _ : int) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Decrement operator (postfix)."""
		...

	def __assign__(self, it : ListIteratorBase[ E, isConst, isReverse ]) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Assignment operator."""
		...

	def __eq__(self, it : ListIteratorBase[ E, isConst, isReverse ]) -> bool:
		"""Equality operator."""
		...

	def pred(self) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Returns predecessor iterator."""
		...

	def succ(self) -> ListIteratorBase[ E, isConst, isReverse ]:
		"""Returns successor iterator."""
		...

	def valid(self) -> bool:
		"""Returns true iff the iterator points to an element."""
		...
