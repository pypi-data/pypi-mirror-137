# file stubs/ogdf/UpwardPlanarSubgraphModule.py generated from classogdf_1_1_upward_planar_subgraph_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanarSubgraphModule(object):

	"""Interface for algorithms for computing an upward planar subgraph."""

	def __init__(self) -> None:
		"""Initializes an upward planar subgraph module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, G : Graph, delEdges : List[edge]) -> None:
		"""Computes set of edgesdelEdgeswhich have to be deleted to obtain the upward planar subgraph."""
		...

	def callAndDelete(self, GC : GraphCopy, delOrigEdges : List[edge]) -> None:
		"""MakesGCupward planar by deleting edges."""
		...

	def __call__(self, G : Graph, delEdges : List[edge]) -> None:
		"""Computes set of edgesdelEdgeswhich have to be deleted to obtain the upward planar subgraph."""
		...
