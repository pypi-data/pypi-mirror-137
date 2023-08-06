# file stubs/ogdf/CPlanarSubgraphModule.py generated from classogdf_1_1_c_planar_subgraph_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarSubgraphModule(ogdf.Module, ogdf.Timeouter):

	"""Interface of algorithms for the computation of c-planar subgraphs."""

	def __init__(self) -> None:
		"""Constructs a cplanar subgraph module."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	@overload
	def call(self, G : ClusterGraph, pCost : EdgeArray[ float ], delEdges : List[edge]) -> ReturnType:
		"""Computes set of edges delEdges, which have to be deleted in order to get a c-planar subgraph."""
		...

	@overload
	def call(self, G : ClusterGraph, delEdges : List[edge]) -> ReturnType:
		"""Computes set of edges delEdges, which have to be deleted in order to get a c-planar subgraph."""
		...

	def doCall(self, CG : ClusterGraph, pCost : EdgeArray[ float ], delEdges : List[edge]) -> ReturnType:
		"""Computes a c-planar subgraph."""
		...
