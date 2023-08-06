# file stubs/ogdf/MinSTCutMaxFlow.py generated from classogdf_1_1_min_s_t_cut_max_flow
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinSTCutMaxFlow(ogdf.MinSTCutModule[ TCost ], Generic[TCost]):

	"""Min-st-cut algorithm, that calculates the cut via maxflow."""

	class cutType(enum.Enum):

		"""The three types of cuts."""

		#: node is in front cut
		FRONT_CUT = enum.auto()

		#: node is in back cut
		BACK_CUT = enum.auto()

		#: node is not part of any cut
		NO_CUT = enum.auto()

	def __init__(self, treatAsUndirected : bool = True, mfModule : MaxFlowModule[ TCost ] = newMaxFlowGoldbergTarjan[ TCost ](), primaryCut : bool = True, calculateOtherCut : bool = True, epsilonTest : EpsilonTest = newEpsilonTest()) -> None:
		"""Constructor."""
		...

	@overload
	def call(self, graph : Graph, weight : EdgeArray[ TCost ], s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...

	@overload
	def call(self, graph : Graph, weights : EdgeArray[ TCost ], flow : EdgeArray[ TCost ], source : node, target : node) -> None:
		"""Partitions the nodes to front- and backcut."""
		...

	@overload
	def call(self, graph : Graph, s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...

	def frontCutIsComplementOfBackCut(self) -> bool:
		"""Returns whether the front cut is the complement of the backcut."""
		...

	def isBackCutEdge(self, e : edge) -> bool:
		"""Returns whether this edge is entering the back cut."""
		...

	def isFrontCutEdge(self, e : edge) -> bool:
		"""Returns whether this edge is leaving the front cut."""
		...

	def isInBackCut(self, v : node) -> bool:
		"""Returns whether this node is part of the back cut."""
		...

	def isInFrontCut(self, v : node) -> bool:
		"""Returns whether this node is part of the front cut."""
		...

	def isOfType(self, v : node, type : cutType) -> bool:
		"""Return whether this node is of the specified type."""
		...

	def setEpsilonTest(self, et : EpsilonTest) -> None:
		"""Assigns a new epsilon test."""
		...
