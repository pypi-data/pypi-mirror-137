# file stubs/ogdf/MaximalPlanarSubgraphSimple.py generated from classogdf_1_1_maximal_planar_subgraph_simple_3_01_t_cost_00_01typename_01std_1_1enable__if_3_01s0944a3a980736a4089122538592aac1c
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MaximalPlanarSubgraphSimple(ogdf.PlanarSubgraphModule[ TCost ], Generic[TCost]):

	"""Naive maximal planar subgraph approach that extends a configurable non-maximal subgraph heuristic."""

	@overload
	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, heuristic : PlanarSubgraphModule[ TCost ]) -> None:
		"""Constructor with user given heuristic that is executed before extending the solution to maximality."""
		...

	def __destruct__(self) -> None:
		"""Desctructor."""
		...

	def clone(self) -> MaximalPlanarSubgraphSimple:
		"""Clone method."""
		...

	def doCall(self, graph : Graph, preferredEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ], preferredImplyPlanar : bool) -> Module.ReturnType:
		"""Computes the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...
