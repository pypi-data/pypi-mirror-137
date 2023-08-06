# file stubs/ogdf/NodeSet.py generated from classogdf_1_1_node_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
OtherSupportsFastSizeQuery = TypeVar('OtherSupportsFastSizeQuery')

SupportFastSizeQuery = TypeVar('SupportFastSizeQuery')

class NodeSet(Generic[SupportFastSizeQuery]):

	"""Node sets."""

	ListType : Type = Union[List[node], ListPure[node]]

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates an empty node set associated with graphG."""
		...

	@overload
	def __init__(self, other : NodeSet[ OtherSupportsFastSizeQuery ]) -> None:
		"""Copy constructor."""
		...

	def clear(self) -> None:
		"""Removes all nodes from this set."""
		...

	def graphOf(self) -> Graph:
		"""Returns the associated graph."""
		...

	def insert(self, v : node) -> None:
		"""Inserts nodevinto this set."""
		...

	def isMember(self, v : node) -> bool:
		"""Returnstrueiff nodevis contained in this set."""
		...

	def nodes(self) -> ListType:
		"""Returns a reference to the list of nodes contained in this set."""
		...

	def __assign__(self, other : NodeSet[ OtherSupportsFastSizeQuery ]) -> NodeSet:
		"""Assignment operator."""
		...

	def remove(self, v : node) -> None:
		"""Removes nodevfrom this set."""
		...

	def size(self) -> int:
		"""Returns the number of nodes in this set."""
		...
