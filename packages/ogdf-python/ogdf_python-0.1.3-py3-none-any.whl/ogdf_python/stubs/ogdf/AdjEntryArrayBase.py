# file stubs/ogdf/AdjEntryArrayBase.py generated from classogdf_1_1_adj_entry_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AdjEntryArrayBase(object):

	"""Abstract base class for adjacency entry arrays."""

	#: The associated graph.
	m_pGraph : Graph = ...

	@overload
	def __init__(self) -> None:
		"""Initializes an adjacency entry array not associated with a graph."""
		...

	@overload
	def __init__(self, base : AdjEntryArrayBase) -> None:
		"""Moves adjacency entry arraybaseto this adjacency entry array."""
		...

	@overload
	def __init__(self, pG : Graph) -> None:
		"""Initializes an adjacency entry array associated withpG."""
		...

	def __destruct__(self) -> None:
		"""Destructor, unregisters the array."""
		...

	def disconnect(self) -> None:
		"""Virtual function called when array is disconnected from the graph."""
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Virtual function called when table size has to be enlarged."""
		...

	def moveRegister(self, base : AdjEntryArrayBase) -> None:
		"""Moves array registration frombaseto this array."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Virtual function called when table has to be reinitialized."""
		...

	def reregister(self, pG : Graph) -> None:
		"""Associates the array with a new graph."""
		...

	def resetIndex(self, newIndex : int, oldIndex : int) -> None:
		"""Virtual function called when the index of an adjacency entry is changed."""
		...
