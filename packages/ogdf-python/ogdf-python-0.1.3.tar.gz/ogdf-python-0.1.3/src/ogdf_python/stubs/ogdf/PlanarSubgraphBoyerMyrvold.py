# file stubs/ogdf/PlanarSubgraphBoyerMyrvold.py generated from classogdf_1_1_planar_subgraph_boyer_myrvold
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarSubgraphBoyerMyrvold(ogdf.PlanarSubgraphModule[  int ]):

	"""Maximum planar subgraph heuristic based on the Boyer-Myrvold planarity test."""

	def __init__(self, runs : int = 1, randomness : float = 0) -> None:
		"""Creates a new Boyer-Myrvold subgraph module."""
		...

	def __destruct__(self) -> None:
		...

	def clone(self) -> PlanarSubgraphBoyerMyrvold:
		...

	def seed(self, rand : std.minstd_rand) -> None:
		"""Seeds the random generator for performing a random DFS. If this method is never called the random generator will be seeded by a value extracted from the global random generator."""
		...

	def doCall(self, graph : Graph, preferedEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[  int ], preferedImplyPlanar : bool) -> ReturnType:
		"""Constructs a planar subgraph according to the options supplied to the constructor."""
		...

	def isRemoved(self, copy : GraphCopy, e : edge) -> bool:
		"""Returns true iff this edge could not be embedded."""
		...
