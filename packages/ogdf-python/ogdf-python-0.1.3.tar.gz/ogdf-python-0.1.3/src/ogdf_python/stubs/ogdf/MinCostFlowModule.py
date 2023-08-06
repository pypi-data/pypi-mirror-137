# file stubs/ogdf/MinCostFlowModule.py generated from classogdf_1_1_min_cost_flow_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinCostFlowModule(Generic[TCost]):

	"""Interface for min-cost flow algorithms."""

	def __init__(self) -> None:
		"""Initializes a min-cost flow module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ], flow : EdgeArray[  int ]) -> bool:
		"""Computes a min-cost flow in the directed graphG."""
		...

	@overload
	def call(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ], flow : EdgeArray[  int ], dual : NodeArray[ TCost ]) -> bool:
		"""Computes a min-cost flow in the directed graphG."""
		...

	@overload
	def checkComputedFlow(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ], flow : EdgeArray[  int ]) -> bool:
		"""checks if a computed flow is a feasible solution to the given problem instance."""
		...

	@overload
	def checkComputedFlow(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ], flow : EdgeArray[  int ], value : TCost) -> bool:
		"""checks if a computed flow is a feasible solution to the given problem instance."""
		...

	def checkProblem(self, G : Graph, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], supply : NodeArray[  int ]) -> bool:
		"""Checks if a given min-cost flow problem instance satisfies the preconditions."""
		...

	def generateProblem(self, G : Graph, n : int, m : int, lowerBound : EdgeArray[  int ], upperBound : EdgeArray[  int ], cost : EdgeArray[ TCost ], supply : NodeArray[  int ]) -> None:
		"""Generates an instance of a min-cost flow problem withnnodes andm+nedges."""
		...
