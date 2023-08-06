# file stubs/ogdf/ShellingOrderSet.py generated from classogdf_1_1_shelling_order_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ShellingOrderSet(ogdf.Array[ node ]):

	"""The node set in a shelling order of a graph."""

	@overload
	def __init__(self) -> None:
		"""Creates an empty shelling order set."""
		...

	@overload
	def __init__(self, n : int, adjL : adjEntry = None, adjR : adjEntry = None) -> None:
		"""Creates a shelling order set fornnodes."""
		...

	def hasLeft(self) -> bool:
		"""Returns true iff the adjacency entry to the left-node exists."""
		...

	def hasRight(self) -> bool:
		"""Returns true iff the adjacency entry to the right-node exists."""
		...

	@overload
	def left(self) -> node:
		"""Returns the left-node of the set."""
		...

	@overload
	def left(self, cl : node) -> None:
		"""Sets the left-node tocl."""
		...

	@overload
	def leftAdj(self) -> adjEntry:
		"""Returns the adjacency entry pointing fromz1to the left node (or 0 if no such node)."""
		...

	@overload
	def leftAdj(self, adjL : adjEntry) -> None:
		"""Sets the adjacency entry pointing to the left-node toadjL."""
		...

	def len(self) -> int:
		"""Returns the length of the order set, i.e., the number of contained nodes."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the i-th node in the order set from left (the leftmost node has index 1)."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the i-th node in the order set from left (the leftmost node has index 1)."""
		...

	@overload
	def right(self) -> node:
		"""Returns the right-node of the set."""
		...

	@overload
	def right(self, cr : node) -> None:
		"""Sets the right-node tocr."""
		...

	@overload
	def rightAdj(self) -> adjEntry:
		"""Returns the adjacency entry pointing fromzpto the right node (or 0 if no such node)."""
		...

	@overload
	def rightAdj(self, adjR : adjEntry) -> None:
		"""Sets the adjacency entry pointing to the right-node toadjR."""
		...
