# file stubs/ogdf/PlanarSubgraphTree.py generated from classogdf_1_1_planar_subgraph_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class PlanarSubgraphTree(ogdf.PlanarSubgraphModule[ TCost ], Generic[TCost]):

	"""Maximum planar subgraph heuristic that yields a spanning tree."""

	def clone(self) -> PlanarSubgraphTree:
		"""Returns a new instance of the planar subgraph module with the same option settings."""
		...

	def doCall(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ], preferredImplyPlanar : bool) -> Module.ReturnType:
		"""Computes the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...
