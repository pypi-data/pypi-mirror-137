# file stubs/ogdf/CPlanarSubClusteredGraph.py generated from classogdf_1_1_c_planar_sub_clustered_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarSubClusteredGraph(object):

	"""Constructs a c-planar subclustered graph of the input based on a spanning tree."""

	def __init__(self) -> None:
		...

	@overload
	def call(self, CG : ClusterGraph, inSub : EdgeArray[ bool ]) -> None:
		...

	@overload
	def call(self, CGO : ClusterGraph, inSub : EdgeArray[ bool ], leftOver : List[edge]) -> None:
		...

	@overload
	def call(self, CGO : ClusterGraph, inSub : EdgeArray[ bool ], leftOver : List[edge], edgeWeight : EdgeArray[ float ]) -> None:
		"""UsesedgeWeightto compute clustered planar subgraph."""
		...
