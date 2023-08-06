# file stubs/ogdf/SubgraphUpwardPlanarizer.py generated from classogdf_1_1_subgraph_upward_planarizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SubgraphUpwardPlanarizer(ogdf.UpwardPlanarizerModule):

	"""Takes an acyclic connected non-upward-planar graph and planarizes it, i.e., we obtain an upward-planar graph where crossings are represented via dummy vertices."""

	#: The acyclic subgraph module.
	m_acyclicMod : std.unique_ptr[AcyclicSubgraphModule] = ...

	#: The edge insertion module.
	m_inserter : std.unique_ptr[UpwardEdgeInserterModule] = ...

	m_runs : int = ...

	#: The upward planar subgraph algorithm.
	m_subgraph : std.unique_ptr[FUPSModule] = ...

	def __init__(self) -> None:
		"""Creates an instance of subgraph planarizer."""
		...

	@overload
	def runs(self) -> int:
		...

	@overload
	def runs(self, n : int) -> None:
		...

	def setAcyclicSubgraphModule(self, acyclicMod : AcyclicSubgraphModule) -> None:
		"""Sets the module option for acyclic subgraph module."""
		...

	def setInserter(self, pInserter : UpwardEdgeInserterModule) -> None:
		"""Sets the module option for the edge insertion module."""
		...

	def setSubgraph(self, FUPS : FUPSModule) -> None:
		"""Sets the module option for the computation of the feasible upward planar subgraph."""
		...

	def doCall(self, UPR : UpwardPlanRep, cost : EdgeArray[  int ], forbid : EdgeArray[ bool ]) -> ReturnType:
		"""Computes an upward planarized representation of the input graph."""
		...
