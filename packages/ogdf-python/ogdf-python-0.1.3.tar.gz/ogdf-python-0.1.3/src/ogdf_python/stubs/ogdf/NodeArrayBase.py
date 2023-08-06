# file stubs/ogdf/NodeArrayBase.py generated from classogdf_1_1_node_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeArrayBase(object):

	"""Abstract base class for node arrays."""

	#: The associated graph.
	m_pGraph : Graph = ...

	@overload
	def __init__(self) -> None:
		"""Initializes an node array not associated with a graph."""
		...

	@overload
	def __init__(self, pG : Graph) -> None:
		"""Initializes an node array associated withpG."""
		...

	@overload
	def __init__(self, base : NodeArrayBase) -> None:
		"""Moves node arraybaseto this node array."""
		...

	def __destruct__(self) -> None:
		...

	def disconnect(self) -> None:
		"""Virtual function called when array is disconnected from the graph."""
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Virtual function called when table size has to be enlarged."""
		...

	def moveRegister(self, base : NodeArrayBase) -> None:
		"""Moves array registration frombaseto this array."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Virtual function called when table has to be reinitialized."""
		...

	def reregister(self, pG : Graph) -> None:
		"""Associates the array with a new graph."""
		...
