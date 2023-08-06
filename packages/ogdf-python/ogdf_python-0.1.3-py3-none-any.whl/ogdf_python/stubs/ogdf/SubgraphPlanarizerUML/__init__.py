# file stubs/ogdf/SubgraphPlanarizerUML/__init__.py generated from classogdf_1_1_subgraph_planarizer_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SubgraphPlanarizerUML(ogdf.UMLCrossingMinimizationModule, ogdf.Logger):

	"""The planarization approach for UML crossing minimization."""

	def doCall(self, pr : PlanRepUML, cc : int, pCostOrig : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		"""Implements the algorithm call."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of subgraph planarizer with default settings."""
		...

	@overload
	def __init__(self, planarizer : SubgraphPlanarizerUML) -> None:
		"""Creates an instance of subgraph planarizer with the same settings asplanarizer."""
		...

	def clone(self) -> UMLCrossingMinimizationModule:
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

	def __assign__(self, planarizer : SubgraphPlanarizerUML) -> SubgraphPlanarizerUML:
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

	def setInserter(self, pInserter : UMLEdgeInsertionModule) -> None:
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
