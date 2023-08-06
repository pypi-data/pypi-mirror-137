# file stubs/ogdf/UMLCrossingMinimizationModule.py generated from classogdf_1_1_u_m_l_crossing_minimization_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UMLCrossingMinimizationModule(ogdf.Module, ogdf.Timeouter):

	"""Base class for UML crossing minimization algorithms."""

	@overload
	def __init__(self) -> None:
		"""Initializes a UML crossing minimization module (default constructor)."""
		...

	@overload
	def __init__(self, cmm : UMLCrossingMinimizationModule) -> None:
		"""Initializes a UML crossing minimization module (copy constructor)."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, prUML : PlanRepUML, cc : int, crossingNumber : int, pCostOrig : EdgeArray[  int ] = None) -> ReturnType:
		"""Computes a planarized representation of the input graph."""
		...

	def clone(self) -> UMLCrossingMinimizationModule:
		"""Returns a new instance of the UML crossing minimization module with the same option settings."""
		...

	def __call__(self, prUML : PlanRepUML, cc : int, crossingNumber : int, pCostOrig : EdgeArray[  int ] = None) -> ReturnType:
		"""Computes a planarized representation of the input graph."""
		...

	def checkCrossingGens(self, prUML : PlanRepUML) -> bool:
		"""Checks if the planarized represenation contains crossing generalizations."""
		...

	def doCall(self, prUML : PlanRepUML, cc : int, pCostOrig : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classes."""
		...
