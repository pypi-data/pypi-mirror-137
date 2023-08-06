# file stubs/ogdf/SListIteratorBase.py generated from classogdf_1_1_s_list_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
isConst = TypeVar('isConst')

# std::enable_if< isConst||!isArgConst, int >::type

isArgConst = TypeVar('isArgConst')

E = TypeVar('E')

class SListIteratorBase(Generic[E, isConst]):

	"""Encapsulates a pointer to anogdf::SListelement."""

	@overload
	def __init__(self) -> None:
		"""Constructs an invalid iterator."""
		...

	@overload
	def __init__(self, it : SListIterator[ E ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, it : SListIteratorBase[ E, isArgConst ]) -> None:
		"""Constructs an iterator that is a copy ofit."""
		...

	@overload
	def __init__(self, pX : ListElem) -> None:
		"""Constructs an iterator that points topX."""
		...

	def __ne__(self, it : SListIteratorBase[ E, isConst ]) -> bool:
		"""Inequality operator."""
		...

	def __deref__(self) -> Elem:
		"""Returns a reference to the element content."""
		...

	def __preinc__(self) -> SListIteratorBase[ E, isConst ]:
		"""Increment operator (prefix)."""
		...

	def __postinc__(self, _ : int) -> SListIteratorBase[ E, isConst ]:
		"""Increment operator (postfix)."""
		...

	def __assign__(self, it : SListIterator[ E ]) -> SListIteratorBase[ E, isConst ]:
		"""Assignment operator."""
		...

	def __eq__(self, it : SListIteratorBase[ E, isConst ]) -> bool:
		"""Equality operator."""
		...

	def succ(self) -> SListIteratorBase[ E, isConst ]:
		"""Returns successor iterator."""
		...

	def valid(self) -> bool:
		"""Returns true iff the iterator points to an element."""
		...
