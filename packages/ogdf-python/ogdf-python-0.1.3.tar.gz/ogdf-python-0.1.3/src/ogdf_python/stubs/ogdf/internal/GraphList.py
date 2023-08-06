# file stubs/ogdf/internal/GraphList.py generated from classogdf_1_1internal_1_1_graph_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T_LIST = TypeVar('T_LIST')

T = TypeVar('T')

class GraphList(ogdf.internal.GraphListBase, Generic[T]):

	"""Lists of graph objects (like nodes, edges, etc.)."""

	def __init__(self) -> None:
		"""Constructs an empty list."""
		...

	def __destruct__(self) -> None:
		"""Destruction: deletes all elements."""
		...

	def clear(self) -> None:
		"""Removes all elements from the list and deletes them."""
		...

	def _del(self, pX : T) -> None:
		"""Removes elementpXfrom the list and deletes it."""
		...

	def delPure(self, pX : T) -> None:
		"""Only removes elementpXfrom the list; does not delete it."""
		...

	def empty(self) -> bool:
		"""Returns true iff the list is empty."""
		...

	def head(self) -> T:
		"""Returns the first element in the list."""
		...

	def insertAfter(self, pX : T, pY : T) -> None:
		"""Inserts elementpXafter elementpY."""
		...

	def insertBefore(self, pX : T, pY : T) -> None:
		"""Inserts elementpXbefore elementpY."""
		...

	@overload
	def move(self, pX : T, L : GraphList[ T ]) -> None:
		"""Moves elementpXto listLand inserts it at the end."""
		...

	@overload
	def move(self, pX : T, L : GraphList[ T ], pY : T, dir : Direction) -> None:
		"""Moves elementpXto listLand inserts it before or afterpY."""
		...

	def moveAfter(self, pX : T, pY : T) -> None:
		"""Moves elementpXfrom its current position to a position afterpY."""
		...

	def moveBefore(self, pX : T, pY : T) -> None:
		"""Moves elementpXfrom its current position to a position beforepY."""
		...

	def pushBack(self, pX : T) -> None:
		"""Adds elementpXat the end of the list."""
		...

	def reverse(self) -> None:
		"""Reverses the order of the list elements."""
		...

	def size(self) -> int:
		"""Returns the size of the list."""
		...

	def sort(self, newOrder : T_LIST) -> None:
		"""Sorts all elements according tonewOrder."""
		...

	def swap(self, pX : T, pY : T) -> None:
		"""Exchanges the positions ofpXandpYin the list."""
		...

	def tail(self) -> T:
		"""Returns the last element in the list."""
		...
