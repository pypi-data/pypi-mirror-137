# file stubs/ogdf/OptimalCrossingMinimizer/__init__.py generated from classogdf_1_1_optimal_crossing_minimizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OptimalCrossingMinimizer(ogdf.optimal_crossing_minimizer.Base):

	#: delegate
	blaster : Master = ...

	def doCall(self, pr : PlanRep, cc : int, pCostOrig : EdgeArray[  int ], pForbiddenOrig : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classes."""
		...

	def onFathom(self, sub : Subproblem) -> None:
		...

	def onTrivialSolution(self) -> None:
		...

	def clone(self) -> CrossingMinimizationModule:
		"""Returns a new instance of the crossing minimization module with the same option settings."""
		...

	@overload
	def master(self) -> Master:
		...

	@overload
	def master(self) -> Master:
		...
