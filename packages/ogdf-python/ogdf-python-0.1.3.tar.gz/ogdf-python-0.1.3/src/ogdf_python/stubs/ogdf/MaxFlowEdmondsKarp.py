# file stubs/ogdf/MaxFlowEdmondsKarp.py generated from classogdf_1_1_max_flow_edmonds_karp
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCap = TypeVar('TCap')

class MaxFlowEdmondsKarp(ogdf.MaxFlowModule[ TCap ], Generic[TCap]):

	"""Computes a max flow via Edmonds-Karp."""

	def computeFlowAfterValue(self) -> None:
		"""Implementation of computeFlowAfterValue from the super class. This does nothing, because the algorithm is finished after computeValue."""
		...

	def computeValue(self, cap : EdgeArray[ TCap ], s : node, t : node) -> TCap:
		"""Implementation of computeValue from the super class. The flow array is cleared,cap,sandtare stored and Edmonds&Karp starts. After this first phase, the flow itself is already computed! Returns 0 if source and sink are identical."""
		...
