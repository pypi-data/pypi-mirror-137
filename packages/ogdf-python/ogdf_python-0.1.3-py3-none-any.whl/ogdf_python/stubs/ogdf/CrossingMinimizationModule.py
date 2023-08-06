# file stubs/ogdf/CrossingMinimizationModule.py generated from classogdf_1_1_crossing_minimization_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingMinimizationModule(ogdf.Module, ogdf.Timeouter):

	"""Base class for crossing minimization algorithms."""

	@overload
	def __init__(self) -> None:
		"""Initializes a crossing minimization module (default constructor)."""
		...

	@overload
	def __init__(self, cmm : CrossingMinimizationModule) -> None:
		"""Initializes an crossing minimization module (copy constructor)."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, pr : PlanRep, cc : int, crossingNumber : int, pCostOrig : EdgeArray[  int ] = None, pForbiddenOrig : EdgeArray[ bool ] = None, pEdgeSubGraphs : EdgeArray[  int ] = None) -> ReturnType:
		"""Computes a planarized representation of the input graph."""
		...

	def clone(self) -> CrossingMinimizationModule:
		"""Returns a new instance of the crossing minimization module with the same option settings."""
		...

	def __call__(self, pr : PlanRep, cc : int, crossingNumber : int, pCostOrig : EdgeArray[  int ] = None, pForbiddenOrig : EdgeArray[ bool ] = None, pEdgeSubGraphs : EdgeArray[  int ] = None) -> ReturnType:
		"""Computes a planarized representation of the input graph."""
		...

	def doCall(self, pr : PlanRep, cc : int, pCostOrig : EdgeArray[  int ], pForbiddenOrig : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classes."""
		...
