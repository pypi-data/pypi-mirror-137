# file stubs/ogdf/steiner_tree/FullComponentStore/__init__.py generated from classogdf_1_1steiner__tree_1_1_full_component_store
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Fun = TypeVar('Fun')

T = TypeVar('T')

ExtraDataType = TypeVar('ExtraDataType')

class FullComponentStore(Generic[T, ExtraDataType]):

	"""A data structure to store full components."""

	#: Listof full components (based on metadata)
	m_components : ArrayBuffer[Metadata[ ExtraDataType ] ] = ...

	#: Our graph representation for the full component store.
	m_graph : EdgeWeightedGraph[ T ] = ...

	#: Incidence vector for terminal nodes.
	m_isTerminal : NodeArray[ bool ] = ...

	#: Mapping of original terminals to m_graph nodes.
	m_nodeCopy : NodeArray[node] = ...

	#: Mapping of m_graph nodes to original nodes.
	m_nodeOrig : NodeArray[node] = ...

	#: The original Steiner instance.
	m_originalGraph : EdgeWeightedGraph[ T ] = ...

	#: The terminal list of the original Steiner instance.
	m_terminals : List[node] = ...

	def copyEdges(self, data : Metadata[ ExtraDataType ], comp : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Copy edges fromcompinto our representation."""
		...

	def copyEdgesWithSimplifiedPaths(self, data : Metadata[ ExtraDataType ], comp : EdgeWeightedGraphCopy[ T ], nonterminals : ArrayBuffer[node]) -> None:
		"""Copy edges fromcompinto our representation, traversing variant to ignore degree-2 nodes."""
		...

	def traverseOverDegree2Nonterminals(self, uO : node, weight : T, marked : EdgeArray[ bool ], adj : adjEntry, comp : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Traverse over degree-2 nonterminals."""
		...

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ]) -> None:
		...

	def cost(self, i : int) -> T:
		"""Returns the sum of edge costs of this full component."""
		...

	def foreachAdjEntry(self, i : int, f : Fun) -> None:
		...

	def foreachEdge(self, id : int, pred : NodeArray[NodeArray[edge]], f : Fun) -> None:
		...

	@overload
	def foreachNode(self, id : int, pred : NodeArray[NodeArray[edge]], f : Fun) -> None:
		...

	@overload
	def foreachNode(self, id : int, f : Fun) -> None:
		...

	def graph(self) -> EdgeWeightedGraph[ T ]:
		...

	def insert(self, comp : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Inserts a component. Note thatcompis copied and degree-2 nodes are removed."""
		...

	def isEmpty(self) -> bool:
		"""Checks if the store does not contain any full components."""
		...

	@overload
	def isTerminal(self, id : int, t : node) -> bool:
		"""checks if a given node t is a terminal in the full component with given id"""
		...

	@overload
	def isTerminal(self, v : node) -> bool:
		...

	def original(self, v : node) -> node:
		...

	def remove(self, id : int) -> None:
		"""Removes a component by itsid."""
		...

	def size(self) -> int:
		"""Returns the number of full components in the store."""
		...

	def start(self, i : int) -> adjEntry:
		...

	def terminals(self, id : int) -> Array[node]:
		"""Returns the list of terminals in the full component with given id."""
		...
