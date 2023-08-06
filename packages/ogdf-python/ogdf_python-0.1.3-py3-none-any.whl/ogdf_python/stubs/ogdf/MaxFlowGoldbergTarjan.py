# file stubs/ogdf/MaxFlowGoldbergTarjan.py generated from classogdf_1_1_max_flow_goldberg_tarjan
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCap = TypeVar('TCap')

class MaxFlowGoldbergTarjan(ogdf.MaxFlowModule[ TCap ], Generic[TCap]):

	"""Computes a max flow via Preflow-Push (global relabeling and gap relabeling heuristic)."""

	def computeFlowAfterValue(self) -> None:
		"""Compute the flow itself after the flow value is already computed. Only used in algorithms with 2 phases. The flow is stored in the array that the user gave in the constructor."""
		...

	def computeValue(self, cap : EdgeArray[ TCap ], s : node, t : node) -> TCap:
		"""Compute only the value of the flow."""
		...
