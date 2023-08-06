# file stubs/ogdf/OrderedOptimalCrossingMinimizer/__init__.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrderedOptimalCrossingMinimizer(ogdf.optimal_crossing_minimizer.Base):

	#: delegate
	blaster : Master = ...

	def hypercubeEggGuy(self, n : int) -> int:
		...

	def toroidalCr(self, n : int, m : int) -> int:
		...

	def doCall(self, pr : PlanRep, cc : int, pCostOrig : EdgeArray[  int ], pForbiddenOrig : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classes."""
		...

	def OGDF_DECLARE_COMPARER(self, _ : EdgeComparer, _ : edge, _ : int, index : WTF_TYPE["x-]"]) -> None:
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
