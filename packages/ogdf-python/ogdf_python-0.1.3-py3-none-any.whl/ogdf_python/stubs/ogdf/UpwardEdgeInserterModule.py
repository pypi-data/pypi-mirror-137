# file stubs/ogdf/UpwardEdgeInserterModule.py generated from classogdf_1_1_upward_edge_inserter_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardEdgeInserterModule(ogdf.Module):

	def __init__(self) -> None:
		"""Initializes an edge insertion module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, UPR : UpwardPlanRep, forbidOriginal : EdgeArray[ bool ], origEdges : List[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given forbidden edges intoUPR."""
		...

	@overload
	def call(self, UPR : UpwardPlanRep, costOrig : EdgeArray[  int ], forbidOriginal : EdgeArray[ bool ], origEdges : List[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given forbidden edges intoUPR."""
		...

	@overload
	def call(self, UPR : UpwardPlanRep, costOrig : EdgeArray[  int ], origEdges : List[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs intoUPR."""
		...

	@overload
	def call(self, UPR : UpwardPlanRep, origEdges : List[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgesintoUPR."""
		...

	def doCall(self, UPR : UpwardPlanRep, origEdges : List[edge], costOrig : EdgeArray[  int ], forbiddenEdgeOrig : EdgeArray[ bool ]) -> ReturnType:
		"""Actual algorithm call that has to be implemented by derived classes."""
		...
