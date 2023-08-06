# file stubs/ogdf/Hashing.py generated from classogdf_1_1_hashing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
H = TypeVar('H')

I = TypeVar('I')

K = TypeVar('K')

class Hashing(ogdf.HashingBase, Generic[K, I, H]):

	"""Hashing with chaining and table doubling."""

	#: The type of const-iterators for hash tables.
	const_iterator : Type = HashConstIterator[ K, I, H ]

	@overload
	def __init__(self, h : Hashing[ K, I, H ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, minTableSize : int = 256, hashFunc : H = H()) -> None:
		"""Creates a hash table for given initial table sizeminTableSize."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def begin(self) -> HashConstIterator[ K, I, H ]:
		"""Returns an hash iterator to the first element in the list of all elements."""
		...

	def clear(self) -> None:
		"""Removes all elements from the hash table."""
		...

	def _del(self, key : K) -> None:
		"""Removes the element with keykeyfrom the hash table (does nothing if no such element)."""
		...

	def empty(self) -> bool:
		"""Returns true iff the table is empty, i.e., contains no elements."""
		...

	def fastInsert(self, key : K, info : I) -> HashElement[ K, I ]:
		"""Inserts a new element with keykeyand informationinfointo the hash table."""
		...

	def insert(self, key : K, info : I) -> HashElement[ K, I ]:
		"""Inserts a new element with keykeyand informationinfointo the hash table."""
		...

	def insertByNeed(self, key : K, info : I) -> HashElement[ K, I ]:
		"""Inserts a new element with keykeyand informationinfointo the hash table."""
		...

	def lookup(self, key : K) -> HashElement[ K, I ]:
		"""Returns the hash element with keykeyin the hash table; returnsnullptrif no such element exists."""
		...

	def member(self, key : K) -> bool:
		"""Returns true iff the hash table contains an element with keykey."""
		...

	def __assign__(self, hashing : Hashing[ K, I, H ]) -> Hashing[ K, I, H ]:
		"""Assignment operator."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the hash table."""
		...

	def firstElement(self, pList : HashElement[ K, I ]) -> HashElement[ K, I ]:
		"""Returns the first element in the list of all elements in the hash table."""
		...

	def nextElement(self, pList : HashElement[ K, I ], pElement : HashElement[ K, I ]) -> HashElement[ K, I ]:
		"""Returns the successor ofpElementin the list of all elements in the hash table."""
		...
