# file stubs/ogdf/LongestPathCompaction.py generated from classogdf_1_1_longest_path_compaction
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LongestPathCompaction(object):

	"""Compaction algorithm using longest paths in the constraint graph."""

	def __init__(self, tighten : bool = True, maxImprovementSteps : int = 0) -> None:
		"""Creates an instance of the longest path compaction algorithm."""
		...

	def constructiveHeuristics(self, PG : PlanRep, OR : OrthoRep, rc : RoutingChannel[  int ], drawing : GridLayoutMapped) -> None:
		"""Constructive heurisitic for orthogonal representations."""
		...

	def improvementHeuristics(self, PG : PlanRep, OR : OrthoRep, rc : RoutingChannel[  int ], drawing : GridLayoutMapped) -> None:
		"""Improvement heurisitic for orthogonal drawings."""
		...

	@overload
	def maxImprovementSteps(self) -> int:
		"""Returns the optionmax improvement steps."""
		...

	@overload
	def maxImprovementSteps(self, maxSteps : int) -> None:
		"""Sets the optionmax improvement steps."""
		...

	@overload
	def tighten(self) -> bool:
		"""Returns the optiontighten."""
		...

	@overload
	def tighten(self, select : bool) -> None:
		"""Sets optiontightentoselect."""
		...
