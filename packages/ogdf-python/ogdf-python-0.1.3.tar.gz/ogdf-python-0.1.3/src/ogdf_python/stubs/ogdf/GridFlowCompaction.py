# file stubs/ogdf/GridFlowCompaction.py generated from classogdf_1_1_grid_flow_compaction
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridFlowCompaction(ogdf.OrthoCompactionModule):

	"""represents compaction algorithm using min-cost flow in the dual of the constraint graph"""

	def __init__(self, maxImprovementSteps : int = 0) -> None:
		"""construction"""
		...

	def callConstructive(self, PG : PlanRep, OR : OrthoRep, drawing : GridLayout) -> None:
		"""call of constructive heuristics for orthogonal representation"""
		...

	def callImprovement(self, PG : PlanRep, OR : OrthoRep, drawing : GridLayout) -> None:
		"""call of improvement heuristics for orthogonal drawing (variable cages)"""
		...

	def improvementHeuristics(self, PG : PlanRep, OR : OrthoRep, drawing : GridLayout, originalSeparation : int) -> None:
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
