# file stubs/ogdf/internal/GraphListBase.py generated from classogdf_1_1internal_1_1_graph_list_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
LIST = TypeVar('LIST')

class GraphListBase(object):

	"""Base class forGraphElementlists."""

	#: Pointer to the first element in the list.
	m_head : GraphElement = ...

	#: The size of the list.
	m_size : int = ...

	#: Pointer to the last element in the list.
	m_tail : GraphElement = ...

	def __init__(self) -> None:
		"""Constructs an empty list."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def _del(self, pX : GraphElement) -> None:
		"""Removes elementpXfrom the list."""
		...

	def insertAfter(self, pX : GraphElement, pY : GraphElement) -> None:
		"""Inserts elementpXafter elementpY."""
		...

	def insertBefore(self, pX : GraphElement, pY : GraphElement) -> None:
		"""Inserts elementpXbefore elementpY."""
		...

	def pushBack(self, pX : GraphElement) -> None:
		"""Adds elementpXat the end of the list."""
		...

	def reverse(self) -> None:
		"""Reverses the order of the list elements."""
		...

	def size(self) -> int:
		"""Returns the size of the list."""
		...

	def sort(self, newOrder : LIST) -> None:
		"""Sorts the list according tonewOrder."""
		...

	def swap(self, pX : GraphElement, pY : GraphElement) -> None:
		"""Exchanges the positions ofpXandpYin the list."""
		...
