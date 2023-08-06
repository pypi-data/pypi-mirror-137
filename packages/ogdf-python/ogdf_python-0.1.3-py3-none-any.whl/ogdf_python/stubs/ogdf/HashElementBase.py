# file stubs/ogdf/HashElementBase.py generated from classogdf_1_1_hash_element_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HashElementBase(object):

	"""Base class for elements within a hash table."""

	def __init__(self, hashValue : size_t) -> None:
		"""Creates a hash element with hash valuehashValue."""
		...

	def hashValue(self) -> size_t:
		"""Returns the hash value of this element."""
		...

	def next(self) -> HashElementBase:
		"""Returns the successor to this element in the list."""
		...
