# file stubs/ogdf/MMSubgraphPlanarizer.py generated from classogdf_1_1_m_m_subgraph_planarizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMSubgraphPlanarizer(ogdf.MMCrossingMinimizationModule):

	"""Planarization approach for minor-monotone crossing minimization."""

	def __init__(self) -> None:
		"""Creates a subgraph planarizer for minor-monotone crossing minimization."""
		...

	@overload
	def permutations(self) -> int:
		"""Returns the number of performed permutations in the edge insertion step."""
		...

	@overload
	def permutations(self, p : int) -> None:
		"""Sets the number of performed permutations in the edge insertion step."""
		...

	def setInserter(self, pInserter : MMEdgeInsertionModule) -> None:
		"""Sets the module option for minor-monotone edge insertion."""
		...

	def setSubgraph(self, pSubgraph : PlanarSubgraphModule[  int ]) -> None:
		"""Sets the module option for the computation of the planar subgraph."""
		...

	def doCall(self, PG : PlanRepExpansion, cc : int, forbid : EdgeArray[ bool ], crossingNumber : int, numNS : int, numSN : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classed."""
		...
