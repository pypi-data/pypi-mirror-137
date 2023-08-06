# file stubs/ogdf/HashArray.py generated from classogdf_1_1_hash_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E = TypeVar('E')

H = TypeVar('H')

I = TypeVar('I')

class HashArray(ogdf.Hashing[ I, E, DefHashFunc[ I ] ], Generic[I, E, H]):

	"""Indexed arrays using hashing for element access."""

	#: The default value for elements.
	const_iterator : Type = HashConstIterator[ I, E, H ]

	@overload
	def __init__(self) -> None:
		"""Creates a hashing array; the default value is the default value of the element type."""
		...

	@overload
	def __init__(self, defaultValue : E, hashFunc : H = H()) -> None:
		"""Creates a hashing array with default valuedefaultValue."""
		...

	@overload
	def __init__(self, A : HashArray[ I, E, H ]) -> None:
		"""Copy constructor."""
		...

	def begin(self) -> HashConstIterator[ I, E, H ]:
		"""Returns an iterator to the first element in the list of all elements."""
		...

	def clear(self) -> None:
		"""Undefines all indices."""
		...

	def empty(self) -> int:
		"""Returns if any indices are defined (= if the hash table is empty)"""
		...

	def isDefined(self, i : I) -> bool:
		"""Returns true iff indexiis defined."""
		...

	def __assign__(self, A : HashArray[ I, E, H ]) -> HashArray[ I, E, H ]:
		"""Assignment operator."""
		...

	@overload
	def __getitem__(self, i : I) -> E:
		"""Returns a reference to the element with indexi."""
		...

	@overload
	def __getitem__(self, i : I) -> E:
		"""Returns the element with indexi."""
		...

	def size(self) -> int:
		"""Returns the number of defined indices (= number of elements in hash table)."""
		...

	def undefine(self, i : I) -> None:
		"""Undefines indexi."""
		...
