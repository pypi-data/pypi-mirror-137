# file stubs/ogdf/FlowCompaction.py generated from classogdf_1_1_flow_compaction
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FlowCompaction(object):

	"""represents compaction algorithm using min-cost flow in the dual of the constraint graph"""

	def __init__(self, maxImprovementSteps : int = 0, costGen : int = 1, costAssoc : int = 1) -> None:
		"""construction"""
		...

	def align(self, b : bool) -> None:
		"""set alignment option"""
		...

	def constructiveHeuristics(self, PG : PlanRep, OR : OrthoRep, rc : RoutingChannel[  int ], drawing : GridLayoutMapped) -> None:
		"""call of constructive heuristics for orthogonal representation"""
		...

	@overload
	def costAssoc(self) -> int:
		"""returns option costGen"""
		...

	@overload
	def costAssoc(self, c : int) -> None:
		"""sets cost of arcs in constraint graph corresponding to associations"""
		...

	@overload
	def costGen(self) -> int:
		"""returns option costGen"""
		...

	@overload
	def costGen(self, c : int) -> None:
		"""sets cost of arcs in constraint graph corresponding to generalizations"""
		...

	@overload
	def improvementHeuristics(self, PG : PlanRep, OR : OrthoRep, rc : RoutingChannel[  int ], drawing : GridLayoutMapped) -> None:
		"""call of improvement heuristics for orthogonal drawing (variable cages)"""
		...

	@overload
	def improvementHeuristics(self, PG : PlanRep, OR : OrthoRep, minDist : MinimumEdgeDistances[  int ], drawing : GridLayoutMapped, originalSeparation : int) -> None:
		"""call of improvement heuristics for orthogonal drawing (tight cages)"""
		...

	@overload
	def maxImprovementSteps(self) -> int:
		"""returns option maxImprovementSteps"""
		...

	@overload
	def maxImprovementSteps(self, maxSteps : int) -> None:
		"""sets option maxImprovementSteps, which is the maximal number of steps performed byimprovementHeuristics()."""
		...

	def scalingSteps(self, sc : int) -> None:
		"""sets number of separation scaling improvement steps"""
		...
