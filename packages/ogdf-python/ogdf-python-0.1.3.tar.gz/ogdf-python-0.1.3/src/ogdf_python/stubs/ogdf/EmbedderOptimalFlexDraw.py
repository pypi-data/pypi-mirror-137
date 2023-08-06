# file stubs/ogdf/EmbedderOptimalFlexDraw.py generated from classogdf_1_1_embedder_optimal_flex_draw
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderOptimalFlexDraw(ogdf.EmbedderModule):

	"""The algorithm computes a planar embedding with minimum cost."""

	def __init__(self) -> None:
		...

	def cost(self, cost : EdgeArray[  int ]) -> None:
		"""Sets bend costs for each edge."""
		...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Calls the embedder algorithm for graphG."""
		...

	def setMinCostFlowComputer(self, pMinCostFlowComputer : MinCostFlowModule[  int ]) -> None:
		"""Sets the module option to compute min-cost flow."""
		...
