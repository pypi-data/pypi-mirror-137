# file stubs/ogdf/PlanRepExpansion/NodeSplit.py generated from classogdf_1_1_plan_rep_expansion_1_1_node_split
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeSplit(object):

	"""Representation of a node split in a planarized expansion."""

	#: This node split's iterator in the list of all node splits.
	m_nsIterator : ListIterator[NodeSplit] = ...

	#: The insertion path of the node split.
	m_path : List[edge] = ...

	@overload
	def __init__(self) -> None:
		"""Creates an empty node split."""
		...

	@overload
	def __init__(self, it : ListIterator[NodeSplit]) -> None:
		"""Creates a node split and sets its iterator in the list of all node splits."""
		...

	def source(self) -> node:
		"""Returns the first node on the node split's insertion path."""
		...

	def target(self) -> node:
		"""Returns the last node on the node split's insertion path."""
		...
