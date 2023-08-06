# file stubs/ogdf/HashConstIterator.py generated from classogdf_1_1_hash_const_iterator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
H = TypeVar('H')

I = TypeVar('I')

K = TypeVar('K')

class HashConstIterator(Generic[K, I, H]):

	"""Iterators for hash tables."""

	@overload
	def __init__(self) -> None:
		"""Creates a hash iterator pointing to no element."""
		...

	@overload
	def __init__(self, it : HashConstIterator[ K, I, H ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, pElement : HashElement[ K, I ], pList : HashElement[ K, I ], pHashing : Hashing[ K, I, H ]) -> None:
		"""Creates a hash iterator pointing to elementpElementin listpListof hash tablepHashing."""
		...

	def info(self) -> I:
		"""Returns the information of the hash element pointed to."""
		...

	def key(self) -> K:
		"""Returns the key of the hash element pointed to."""
		...

	def __preinc__(self) -> HashConstIterator[ K, I, H ]:
		"""Moves this hash iterator to the next element (iterator gets invalid if no more elements)."""
		...

	def __assign__(self, it : HashConstIterator[ K, I, H ]) -> HashConstIterator:
		"""Assignment operator."""
		...

	def valid(self) -> bool:
		"""Returns true if the hash iterator points to an element."""
		...
