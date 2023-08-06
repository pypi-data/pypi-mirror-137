# file stubs/ogdf/SubgraphPlanarizer/__init__.py generated from classogdf_1_1_subgraph_planarizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SubgraphPlanarizer(ogdf.CrossingMinimizationModule, ogdf.Logger):

	"""The planarization approach for crossing minimization."""

	def doCall(self, pr : PlanRep, cc : int, pCostOrig : EdgeArray[  int ], pForbiddenOrig : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Implements the algorithm call."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of subgraph planarizer with default settings."""
		...

	@overload
	def __init__(self, planarizer : SubgraphPlanarizer) -> None:
		"""Creates an instance of subgraph planarizer with the same settings asplanarizer."""
		...

	def clone(self) -> CrossingMinimizationModule:
		"""Returns a new instance of subgraph planarizer with the same option settings."""
		...

	@overload
	def maxThreads(self) -> int:
		"""Returns the maximal number of used threads."""
		...

	@overload
	def maxThreads(self, n : int) -> None:
		"""Sets the maximal number of used threads ton."""
		...

	def __assign__(self, planarizer : SubgraphPlanarizer) -> SubgraphPlanarizer:
		"""Assignment operator. Copies option settings only."""
		...

	@overload
	def permutations(self) -> int:
		"""Returns the number of permutations."""
		...

	@overload
	def permutations(self, p : int) -> None:
		"""Sets the number of permutations top."""
		...

	def setInserter(self, pInserter : EdgeInsertionModule) -> None:
		"""Sets the module option for the edge insertion module."""
		...

	def setSubgraph(self, pSubgraph : PlanarSubgraphModule[  int ]) -> None:
		"""Sets the module option for the computation of the planar subgraph."""
		...

	@overload
	def setTimeout(self) -> bool:
		"""Returns the current setting of optionssetTimeout."""
		...

	@overload
	def setTimeout(self, b : bool) -> None:
		"""Sets the optionsetTimeouttob."""
		...
