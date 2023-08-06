# file stubs/ogdf/OrderedOptimalCrossingMinimizer/Master/__init__.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Master(ogdf.optimal_crossing_minimizer.MasterBase):

	crossingVariableComparer : CrossingVariableComparer = ...

	edgeComparer : EdgeComparer = ...

	inducedCrossingConfiguration : CrossingConfiguration = ...

	def __init__(self) -> None:
		...

	def enumerationStrategy(self, s1 : abacus.Sub, s2 : abacus.Sub) -> int:
		"""Analyzes the enumeration strategy set in the parameter file.abacusand calls the corresponding comparison function for the subproblemss1ands2."""
		...

	def firstSub(self) -> abacus.Sub:
		"""Should return a pointer to the first subproblem of the optimization, i.e., the root node of the enumeration tree."""
		...

	def getStartHeuristic(self) -> CrossingMinimizationModule:
		...

	@overload
	def hintEffects(self) -> int:
		...

	@overload
	def hintEffects(self, h : int) -> None:
		...

	def initializeOptimization(self) -> None:
		"""The default implementation ofinitializeOptimization()does nothing."""
		...

	def doCall(self, PG : PlanRep, cc : int, cost : EdgeArray[  int ], forbid : EdgeArray[ bool ], crossingNumber : int) -> ReturnType:
		...
