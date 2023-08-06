# file stubs/ogdf/HashingBase.py generated from classogdf_1_1_hashing_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HashingBase(object):

	"""Base class for hashing with chaining and table doubling."""

	#: The current number of elements.
	m_count : int = ...

	#: The current table size minus one.
	m_hashMask : int = ...

	#: The minimal table size.
	m_minTableSize : int = ...

	#: The hash table (an array of lists).
	m_table : HashElementBase = ...

	#: The current table size.
	m_tableSize : int = ...

	#: The maximal number of elements at this table size.
	m_tableSizeHigh : int = ...

	#: The minimal number of elements at this table size.
	m_tableSizeLow : int = ...

	@overload
	def __init__(self, H : HashingBase) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, minTableSize : int) -> None:
		"""Creates a hash table with minimum table sizeminTableSize."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def clear(self) -> None:
		"""Removes all elements from the hash table."""
		...

	def _del(self, pElement : HashElementBase) -> None:
		"""Removes the elementpElementfrom the hash table."""
		...

	def empty(self) -> int:
		"""Returns if the hash table is empty."""
		...

	def firstElement(self, pList : HashElementBase) -> HashElementBase:
		"""Returns the first element in the list of all elements in the hash table."""
		...

	def firstListElement(self, hashValue : size_t) -> HashElementBase:
		"""Returns the first element in the list for elements with hash valuehashValue."""
		...

	def insert(self, pElement : HashElementBase) -> None:
		"""Inserts a new elementpElementinto the hash table."""
		...

	def nextElement(self, pList : HashElementBase, pElement : HashElementBase) -> HashElementBase:
		"""Returns the successor ofpElementin the list of all elements in the hash table."""
		...

	def __assign__(self, H : HashingBase) -> HashingBase:
		"""Assignment operator."""
		...

	def resize(self, newTableSize : int) -> None:
		"""Resizes the hash table tonewTableSize."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the hash table."""
		...

	def copy(self, pElement : HashElementBase) -> HashElementBase:
		"""Called to create a copy of the elementpElement."""
		...

	def destroy(self, pElement : HashElementBase) -> None:
		"""Called to delete hash element."""
		...

	def destroyAll(self) -> None:
		"""Deletes all elements in hash table (but does not free m_table!)."""
		...
