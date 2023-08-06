# file stubs/ogdf/HashElement.py generated from classogdf_1_1_hash_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
I = TypeVar('I')

K = TypeVar('K')

class HashElement(ogdf.HashElementBase, Generic[K, I]):

	"""Representation of elements in a hash table."""

	def __init__(self, hashValue : size_t, key : K, info : I) -> None:
		"""Creates a hash element with given hash value, key, and information."""
		...

	@overload
	def info(self) -> I:
		"""Returns a refeence to the information value."""
		...

	@overload
	def info(self) -> I:
		"""Returns the information value."""
		...

	def key(self) -> K:
		"""Returns the key value."""
		...

	def next(self) -> HashElement[ K, I ]:
		"""Returns the successor element in the list."""
		...
