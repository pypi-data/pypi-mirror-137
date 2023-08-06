# file stubs/ogdf/PlanarSubgraphCactus.py generated from classogdf_1_1_planar_subgraph_cactus
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class PlanarSubgraphCactus(ogdf.PlanarSubgraphTriangles[ TCost ], Generic[TCost]):

	"""Maximum planar subgraph approximation algorithm by Calinescu et al."""

	def __init__(self) -> None:
		...

	def clone(self) -> PlanarSubgraphCactus:
		"""Returns a new instance of the planarization module with the same settings."""
		...
