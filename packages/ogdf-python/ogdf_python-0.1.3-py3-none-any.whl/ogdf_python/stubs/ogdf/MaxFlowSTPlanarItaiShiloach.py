# file stubs/ogdf/MaxFlowSTPlanarItaiShiloach.py generated from classogdf_1_1_max_flow_s_t_planar_itai_shiloach
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCap = TypeVar('TCap')

class MaxFlowSTPlanarItaiShiloach(ogdf.MaxFlowModule[ TCap ], Generic[TCap]):

	"""Computes a max flow in s-t-planar network via uppermost paths."""

	def __destruct__(self) -> None:
		"""Free allocated ressources."""
		...

	def computeFlowAfterValue(self) -> None:
		"""Computes the actual flow on each edge."""
		...

	def computeValue(self, originalCapacities : EdgeArray[ TCap ], source : node, target : node) -> TCap:
		"""Computes the maximal flow from source to sink."""
		...
