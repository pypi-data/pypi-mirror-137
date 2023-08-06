# file stubs/ogdf/cluster_planarity/CPlanarSubClusteredST.py generated from classogdf_1_1cluster__planarity_1_1_c_planar_sub_clustered_s_t
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarSubClusteredST(object):

	"""Constructs a c-planar subclustered spanning tree of the input by setting edgearray values."""

	def __init__(self) -> None:
		...

	@overload
	def call(self, CG : ClusterGraph, inST : EdgeArray[ bool ]) -> None:
		"""sets values in inST according to membership in c-planar STGraph"""
		...

	@overload
	def call(self, CG : ClusterGraph, inST : EdgeArray[ bool ], weight : EdgeArray[ float ]) -> None:
		"""sets values in inST according to membership in c-planar STGraph, computes minimum spanning tree according to weight inweight"""
		...
