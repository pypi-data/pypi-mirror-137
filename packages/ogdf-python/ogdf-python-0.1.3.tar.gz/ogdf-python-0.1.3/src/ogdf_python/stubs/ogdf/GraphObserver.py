# file stubs/ogdf/GraphObserver.py generated from classogdf_1_1_graph_observer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphObserver(object):

	"""Abstract Base class for graph observers."""

	#: watched graph
	m_itGList : ListIterator[GraphObserver] = ...

	m_pGraph : Graph = ...

	@overload
	def __init__(self) -> None:
		"""Constructs instance ofGraphObserverclass."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs instance ofGraphObserverclass."""
		...

	def __destruct__(self) -> None:
		"""Destroys the instance, unregisters it from watched graph."""
		...

	def cleared(self) -> None:
		"""Called by watched graph when its clear function is called Has to be implemented by derived classes."""
		...

	def edgeAdded(self, e : edge) -> None:
		"""Called by watched graph when an edge is added Has to be implemented by derived classes."""
		...

	def edgeDeleted(self, e : edge) -> None:
		"""Called by watched graph when an edge is deleted Has to be implemented by derived classes."""
		...

	def getGraph(self) -> Graph:
		...

	def nodeAdded(self, v : node) -> None:
		"""Called by watched graph when a node is added Has to be implemented by derived classes."""
		...

	def nodeDeleted(self, v : node) -> None:
		"""Called by watched graph when a node is deleted Has to be implemented by derived classes."""
		...

	def reInit(self) -> None:
		"""Called by watched graph when it is reinitialized Has to be implemented by derived classes."""
		...

	def reregister(self, pG : Graph) -> None:
		"""Associates observer instance with graphG."""
		...
