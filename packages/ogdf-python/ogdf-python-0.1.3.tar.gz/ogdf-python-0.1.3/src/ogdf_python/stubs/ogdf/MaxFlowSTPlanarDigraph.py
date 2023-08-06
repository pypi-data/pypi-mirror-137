# file stubs/ogdf/MaxFlowSTPlanarDigraph.py generated from classogdf_1_1_max_flow_s_t_planar_digraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCap = TypeVar('TCap')

class MaxFlowSTPlanarDigraph(ogdf.MaxFlowModule[ TCap ], Generic[TCap]):

	"""Computes a max flow in s-t-planar network via dual shortest paths."""

	def computeFlowAfterValue(self) -> None:
		"""Implementation of computeFlowAfterValue from the super class. This does nothing, because the algorithm is finished after computeValue."""
		...

	def computeValue(self, cap : EdgeArray[ TCap ], s : node, t : node) -> TCap:
		"""Compute only the value of the flow."""
		...

	def init(self, graph : Graph, flow : EdgeArray[ TCap ] = None) -> None:
		"""Initialize the problem with a graph and optional flow array. If noflowarray is given, a new ("internal") array will be created. If aflowarray is given, the algorithm uses this "external" array."""
		...
