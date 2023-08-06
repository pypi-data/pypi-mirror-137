# file stubs/ogdf/HypergraphArrayBase.py generated from classogdf_1_1_hypergraph_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphArrayBase(object):

	"""Abstract base class for hypergraph arrays."""

	#: The associated hypergraph.
	m_hypergraph : Hypergraph = ...

	#: Pointer to list element in the list of all registered hypergraph arrays which references this array.
	m_it : ListIterator[HypergraphArrayBase] = ...

	@overload
	def __init__(self) -> None:
		"""Initializes an array not associated with a hypergraph."""
		...

	@overload
	def __init__(self, pH : Hypergraph) -> None:
		"""Initializes an array associated withpH."""
		...

	def __destruct__(self) -> None:
		"""Destructor, unregisters the array."""
		...

	def disconnect(self) -> None:
		"""Disconnetion from the hypergraph."""
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Table size enlargement."""
		...

	def hypergraphOf(self) -> Hypergraph:
		"""Returns a pointer to the associated hypergraph."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Table re-initialization."""
		...

	def reregister(self, H : Hypergraph) -> None:
		"""Associates the array with a new hypergraph."""
		...
