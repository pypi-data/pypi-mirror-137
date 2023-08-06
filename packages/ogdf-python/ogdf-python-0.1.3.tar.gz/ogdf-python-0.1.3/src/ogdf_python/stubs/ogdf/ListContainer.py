# file stubs/ogdf/ListContainer.py generated from classogdf_1_1_list_container
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Master = TypeVar('Master')

E = TypeVar('E')

class ListContainer(ogdf.List[ E ], Generic[E, Master]):

	#: Provides a bidirectional iterator to an object in the container.
	iterator : Type = List[ E ].const_iterator

	#: Provides a bidirectional reverse iterator to an object in the container.
	reverse_iterator : Type = List[ E ].const_reverse_iterator

	def begin(self) -> iterator:
		"""Returns an iterator to the first element in the container."""
		...

	def end(self) -> iterator:
		"""Returns an iterator to the one-past-last element in the container."""
		...

	def rbegin(self) -> reverse_iterator:
		"""Returns a reverse iterator to the last element in the container."""
		...

	def rend(self) -> reverse_iterator:
		"""Returns a reverse iterator to the one-before-first element in the container."""
		...

	def size(self) -> int:
		"""Returns the number of elements in the container."""
		...
