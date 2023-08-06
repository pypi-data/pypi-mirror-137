# file stubs/ogdf/ArrayReverseIteratorBase.py generated from classogdf_1_1_array_reverse_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
# std::enable_if< isConstSFINAE, int >::type

E = TypeVar('E')

isConstSFINAE = TypeVar('isConstSFINAE')

isArgConst = TypeVar('isArgConst')

isConst = TypeVar('isConst')

# std::enable_if< isConst||!isArgConst, int >::type

class ArrayReverseIteratorBase(Generic[E, isConst]):

	"""Random-access reverse iterator based on a pointer to an array element."""

	@overload
	def __init__(self) -> None:
		"""Constructs an invalid iterator."""
		...

	@overload
	def __init__(self, it : ArrayReverseIteratorBase[ E, isArgConst ]) -> None:
		"""Constructs an iterator that is a copy ofit."""
		...

	@overload
	def __init__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> None:
		"""Copy constructor. clang10 does not see the above templated one match this case and requires it explicitly."""
		...

	@overload
	def __init__(self, pX : E) -> None:
		"""Constructs an iterator that points to const E*pX."""
		...

	@overload
	def __init__(self, pX : E) -> None:
		"""Constructs an iterator that points to E*pX."""
		...

	def stdconditionalisConstEE(self) -> None:
		"""Implicit cast to (const) E*."""
		...

	def __ne__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Inequality operator."""
		...

	def __deref__(self) -> Elem:
		"""Returns the element this iterator points to."""
		...

	def __add__(self, rhs : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Addition operator with int on the right-hand side."""
		...

	def __preinc__(self) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Increment operator (prefix)."""
		...

	def __postinc__(self, _ : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Increment operator (postfix)."""
		...

	def __iadd__(self, rhs : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Compound assignment operator (+)."""
		...

	@overload
	def __sub__(self, rhs : ArrayReverseIteratorBase[ E, isArgConst ]) -> int:
		"""Subtraction operator."""
		...

	@overload
	def __sub__(self, rhs : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Subtraction operator with int on the right-hand side."""
		...

	def __predec__(self) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Decrement operator (prefix)."""
		...

	def __postdec__(self, _ : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Decrement operator (postfix)."""
		...

	def __isub__(self, rhs : int) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Compound assignment operator (-)."""
		...

	def __lt__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Less-than operator."""
		...

	def __le__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Less-than-or-equals operator."""
		...

	def __assign__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> ArrayReverseIteratorBase[ E, isConst ]:
		"""Assignment operator."""
		...

	def __eq__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Equality operator."""
		...

	def __gt__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Greater-than operator."""
		...

	def __ge__(self, it : ArrayReverseIteratorBase[ E, isConst ]) -> bool:
		"""Greater-than-or-equals operator."""
		...

	@overload
	def __getitem__(self, idx : std.size_t) -> Elem:
		"""Member access operator."""
		...

	@overload
	def __getitem__(self, idx : std.size_t) -> Elem:
		"""Const member access operator."""
		...
