# file stubs/ogdf/MinCostFlowReinelt/__init__.py generated from classogdf_1_1_min_cost_flow_reinelt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinCostFlowReinelt(ogdf.MinCostFlowModule[ TCost ], Generic[TCost]):

	"""Computes a min-cost flow using a network simplex method."""

	def __init__(self) -> None:
		...

	def call(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ], flow : EdgeArray[  int ], dual : NodeArray[ TCost ]) -> bool:
		"""Computes a min-cost flow in the directed graphGusing a network simplex method."""
		...

	def infinity(self) -> int:
		...
