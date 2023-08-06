# file stubs/ogdf/MaxFlowPlanarErickson.py generated from classogdf_1_1_max_flow_planar_erickson
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCap = TypeVar('TCap')

class MaxFlowPlanarErickson(ogdf.MaxFlowModule[ TCap ], Generic[TCap]):

	"""Computes a max flow in non-s-t-planar network via dual shortest paths and interdigitating spannning trees."""

	@overload
	def __init__(self) -> None:
		"""Empty Constructor."""
		...

	@overload
	def __init__(self, graph : Graph, flow : EdgeArray[ TCap ] = None) -> None:
		"""Constructor that calls init."""
		...

	def computeFlowAfterValue(self) -> None:
		"""Implementation of computeFlowAfterValue from the super class. This does nothing, because the algorithm is finished after computeValue."""
		...

	def computeValue(self, cap : EdgeArray[ TCap ], s : node, t : node) -> TCap:
		"""Implementation of computeValue from the super class. The flow array is cleared,cap,sandtare stored and Erickson's algo. starts. After this first phase, the flow itself is already computed!"""
		...

	def init(self, graph : Graph, flow : EdgeArray[ TCap ] = None) -> None:
		"""Initialize the problem with a graph and optional flow array. Just callsMaxFlowModule<TCap>::init."""
		...
