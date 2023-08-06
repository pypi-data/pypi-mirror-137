# file stubs/ogdf/UpwardPlanarSubgraphSimple.py generated from classogdf_1_1_upward_planar_subgraph_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanarSubgraphSimple(ogdf.UpwardPlanarSubgraphModule):

	"""A maximal planar subgraph algorithm using planarity testing."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, delEdges : List[edge]) -> None:
		"""Computes set of edgesdelEdgeswhich have to be deleted to obtain the upward planar subgraph."""
		...

	@overload
	def call(self, GC : GraphCopy, delEdges : List[edge]) -> None:
		...
