# file stubs/ogdf/PlanarSubgraphTriangles.py generated from classogdf_1_1_planar_subgraph_triangles
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class PlanarSubgraphTriangles(ogdf.PlanarSubgraphModule[ TCost ], Generic[TCost]):

	"""Maximum planar subgraph approximation algorithms by Chalermsook/Schmid and Calinescu et al."""

	def __init__(self, onlyTriangles : bool = False) -> None:
		"""Creates a planarization module based on triangle or diamond matching."""
		...

	def clone(self) -> PlanarSubgraphTriangles:
		"""Returns a new instance of the planarization module with the same settings."""
		...

	def doCall(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ], preferredImplyPlanar : bool = False) -> Module.ReturnType:
		"""Computes the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...
