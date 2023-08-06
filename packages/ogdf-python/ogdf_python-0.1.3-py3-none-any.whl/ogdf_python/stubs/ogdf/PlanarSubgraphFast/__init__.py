# file stubs/ogdf/PlanarSubgraphFast/__init__.py generated from classogdf_1_1_planar_subgraph_fast
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class PlanarSubgraphFast(ogdf.PlanarSubgraphModule[ TCost ], Generic[TCost]):

	"""Computation of a planar subgraph using PQ-trees."""

	def __init__(self) -> None:
		"""Creates an instance of the fast planar subgraph algorithm with default settings (runs= 10)."""
		...

	def clone(self) -> PlanarSubgraphFast:
		"""Returns a new instance of fast planar subgraph with the same option settings."""
		...

	@overload
	def runs(self) -> int:
		"""Returns the current number of randomized runs."""
		...

	@overload
	def runs(self, nRuns : int) -> None:
		"""Sets the number of randomized runs tonRuns."""
		...

	def doCall(self, G : Graph, preferedEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ], preferedImplyPlanar : bool) -> Module.ReturnType:
		"""Returns true, if G is planar, false otherwise."""
		...
