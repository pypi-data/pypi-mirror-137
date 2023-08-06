# file stubs/ogdf/Reverse.py generated from classogdf_1_1_reverse
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Reverse(Generic[T]):

	"""A wrapper class to easily iterate through a container in reverse."""

	#: Provides a reverse iterator disguised a normal iterator.
	iterator : Type = Union[T.const_reverse_iterator, T.reverse_iterator]

	def __init__(self, container : T) -> None:
		"""Creates a reverse iteration wrapper forcontainer."""
		...

	def begin(self) -> iterator:
		"""Returns a reverse iterator to the last element ofm_container."""
		...

	def end(self) -> iterator:
		"""Returns a reverse iterator to the one-before-first element ofm_container."""
		...
