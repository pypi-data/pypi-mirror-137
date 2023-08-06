# file stubs/ogdf/HypergraphObserver.py generated from classogdf_1_1_hypergraph_observer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphObserver(object):

	#: Observed hypergraph.
	m_hypergraph : Hypergraph = ...

	#: Listof all registered hypergraph observers.
	m_itObserver : ListIterator[HypergraphObserver] = ...

	@overload
	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, pH : Hypergraph) -> None:
		"""Constructor assigningpHhypergraph to the observer."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def cleared(self) -> None:
		"""Called by the observed hypergraph when it is cleared."""
		...

	def hyperedgeAdded(self, e : hyperedge) -> None:
		"""Called by an observed hypergraph when a hyperedge is added."""
		...

	def hyperedgeDeleted(self, e : hyperedge) -> None:
		"""Called by an observed hypergraph when a hyperedge is deleted."""
		...

	def hypergraph(self) -> Hypergraph:
		"""Returns the observer hypergraph."""
		...

	def hypernodeAdded(self, v : hypernode) -> None:
		"""Called by an observed hypergraph when a hypernode is added."""
		...

	def hypernodeDeleted(self, v : hypernode) -> None:
		"""Called by an observed hypergraph when a hypernode is deleted."""
		...

	def init(self, pH : Hypergraph) -> None:
		"""Associates an observer instance with hypergraphpH."""
		...
