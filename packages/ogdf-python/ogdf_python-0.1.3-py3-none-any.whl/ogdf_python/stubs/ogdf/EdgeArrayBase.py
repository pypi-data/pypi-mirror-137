# file stubs/ogdf/EdgeArrayBase.py generated from classogdf_1_1_edge_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeArrayBase(object):

	"""Abstract base class for edge arrays."""

	#: The associated graph.
	m_pGraph : Graph = ...

	@overload
	def __init__(self) -> None:
		"""Initializes an edge array not associated with a graph."""
		...

	@overload
	def __init__(self, pG : Graph) -> None:
		"""Initializes an edge array associated withpG."""
		...

	@overload
	def __init__(self, base : EdgeArrayBase) -> None:
		"""Moves edge arraybaseto this edge array."""
		...

	def __destruct__(self) -> None:
		...

	def disconnect(self) -> None:
		"""Virtual function called when array is disconnected from the graph."""
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Virtual function called when table size has to be enlarged."""
		...

	def moveRegister(self, base : EdgeArrayBase) -> None:
		"""Moves array registration frombaseto this array."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Virtual function called when table has to be reinitialized."""
		...

	def reregister(self, pG : Graph) -> None:
		"""Associates the array with a new graph."""
		...
