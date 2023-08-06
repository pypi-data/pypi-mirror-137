# file stubs/ogdf/DynamicBacktrack.py generated from classogdf_1_1_dynamic_backtrack
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicBacktrack(object):

	"""Extracts all possible paths with backtracking using given edges and special constraints."""

	class KuratowskiFlag(enum.Enum):

		"""Marks an edge with three Flags: externalPath, pertinentPath and/or singlePath."""

		externalPath = enum.auto()

		pertinentPath = enum.auto()

		singlePath = enum.auto()

	#: The one and only DFI-NodeArray.
	m_dfi : NodeArray[  int ] = ...

	#: Identifies endnodes.
	m_end : node = ...

	#: Every traversed edge has to be signed with this flag.
	m_flag : int = ...

	#: Flags, that partition the edges into pertinent and external subgraphs.
	m_flags : EdgeArray[  int ] = ...

	#: Iff true, DFI of endnodes has to be <DFI[end], otherwise the only valid endnode isend.
	m_less : bool = ...

	#: Saves the parent edge for each node in path.
	m_parent : NodeArray[adjEntry] = ...

	#: Start node of backtracking.
	m_start : node = ...

	#: Backtracking stack. A nullptr-element indicates a return from a child node.
	stack : ArrayBuffer[adjEntry] = ...

	def __init__(self, g : Graph, dfi : NodeArray[  int ], flags : EdgeArray[  int ]) -> None:
		"""Constructor."""
		...

	def addNextPath(self, list : SListPure[edge], endnode : node) -> bool:
		"""Returns next possible path fromstart-toendnode, if exists."""
		...

	def addNextPathExclude(self, list : SListPure[edge], endnode : node, nodeflags : NodeArray[  int ], exclude : int, exceptOnEdge : int) -> bool:
		"""Returns next possible path under constraints fromstart-toendnode, if exists."""
		...

	def init(self, start : node, end : node, less : bool, flag : int, startFlag : int, startInclude : edge, startExlude : edge) -> None:
		"""Reinitializes backtracking with new constraints. All paths will be traversed again."""
		...

	def __assign__(self, _ : DynamicBacktrack) -> DynamicBacktrack:
		"""Assignment is not defined!"""
		...
