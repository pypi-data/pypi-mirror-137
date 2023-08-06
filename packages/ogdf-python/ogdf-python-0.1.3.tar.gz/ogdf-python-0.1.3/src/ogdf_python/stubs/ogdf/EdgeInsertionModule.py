# file stubs/ogdf/EdgeInsertionModule.py generated from classogdf_1_1_edge_insertion_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeInsertionModule(ogdf.Module, ogdf.Timeouter):

	"""Interface for edge insertion algorithms."""

	@overload
	def __init__(self) -> None:
		"""Initializes an edge insertion module (default constructor)."""
		...

	@overload
	def __init__(self, eim : EdgeInsertionModule) -> None:
		"""Initializes an edge insertion module (copy constructor)."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	@overload
	def call(self, pr : PlanRepLight, origEdges : Array[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgesintopr."""
		...

	@overload
	def call(self, pr : PlanRepLight, forbiddenOrig : EdgeArray[ bool ], origEdges : Array[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given forbidden edges intopr."""
		...

	@overload
	def call(self, pr : PlanRepLight, costOrig : EdgeArray[  int ], origEdges : Array[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs intopr."""
		...

	@overload
	def call(self, pr : PlanRepLight, costOrig : EdgeArray[  int ], origEdges : Array[edge], edgeSubGraphs : EdgeArray[  int ]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs and subgraphs (for simultaneous drawing) intopr."""
		...

	@overload
	def call(self, pr : PlanRepLight, costOrig : EdgeArray[  int ], forbiddenOrig : EdgeArray[ bool ], origEdges : Array[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs and forbidden edges intopr."""
		...

	@overload
	def call(self, pr : PlanRepLight, costOrig : EdgeArray[  int ], forbiddenOrig : EdgeArray[ bool ], origEdges : Array[edge], edgeSubGraphs : EdgeArray[  int ]) -> ReturnType:
		"""Inserts all edges inorigEdgeswith given costs, forbidden edges, and subgraphs (for simultaneous drawing) intopr."""
		...

	def callEx(self, pr : PlanRepLight, origEdges : Array[edge], pCostOrig : EdgeArray[  int ] = None, pForbiddenOrig : EdgeArray[ bool ] = None, pEdgeSubGraphs : EdgeArray[  int ] = None) -> ReturnType:
		"""Inserts all edges inorigEdgesintopr, optionally costs, forbidden edges, and subgraphs (for simultaneous drawing) may be given."""
		...

	def clone(self) -> EdgeInsertionModule:
		"""Returns a new instance of the edge insertion module with the same option settings."""
		...

	def doCall(self, pr : PlanRepLight, origEdges : Array[edge], pCostOrig : EdgeArray[  int ], pForbiddenOrig : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ]) -> ReturnType:
		"""Actual algorithm call that has to be implemented by derived classes."""
		...
