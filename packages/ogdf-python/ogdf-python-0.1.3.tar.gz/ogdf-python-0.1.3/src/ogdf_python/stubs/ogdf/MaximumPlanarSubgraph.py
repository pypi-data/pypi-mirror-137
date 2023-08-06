# file stubs/ogdf/MaximumPlanarSubgraph.py generated from classogdf_1_1_maximum_planar_subgraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MaximumPlanarSubgraph(ogdf.PlanarSubgraphModule[ TCost ], Generic[TCost]):

	"""Exact computation of a maximum planar subgraph."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def clone(self) -> MaximumPlanarSubgraph:
		"""Returns a new instance of the planar subgraph module with the same option settings."""
		...

	def doCall(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ], preferredImplyPlanar : bool) -> Module.ReturnType:
		"""Computes the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...
