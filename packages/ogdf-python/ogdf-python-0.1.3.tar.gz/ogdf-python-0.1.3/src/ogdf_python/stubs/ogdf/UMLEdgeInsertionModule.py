# file stubs/ogdf/UMLEdgeInsertionModule.py generated from classogdf_1_1_u_m_l_edge_insertion_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UMLEdgeInsertionModule(ogdf.Module, ogdf.Timeouter):

	"""Interface for UML edge insertion algorithms."""

	@overload
	def __init__(self) -> None:
		"""Initializes a UML edge insertion module (default constructor)."""
		...

	@overload
	def __init__(self, eim : UMLEdgeInsertionModule) -> None:
		"""Initializes a UML edge insertion module (copy constructor)."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	@overload
	def call(self, pr : PlanRepLight, origEdges : Array[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgesintoprwhile avoiding crossings between generalizations."""
		...

	@overload
	def call(self, pr : PlanRepLight, origEdges : Array[edge], costOrig : EdgeArray[  int ]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs intoprwhile avoiding crossings between generalizations."""
		...

	def callEx(self, pr : PlanRepLight, origEdges : Array[edge], pCostOrig : EdgeArray[  int ] = None, pEdgeSubGraphs : EdgeArray[  int ] = None) -> ReturnType:
		"""Inserts all edges inorigEdgesintoprwhile avoiding crossings between generalizations, optionally costs and subgraphs may be given."""
		...

	def clone(self) -> UMLEdgeInsertionModule:
		"""Returns a new instance of the UML edge insertion module with the same option settings."""
		...

	def doCall(self, pr : PlanRepLight, origEdges : Array[edge], pCostOrig : EdgeArray[  int ], pEdgeSubGraphs : EdgeArray[  int ]) -> ReturnType:
		"""Actual algorithm call that has to be implemented by derived classes."""
		...
