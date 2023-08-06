# file stubs/ogdf/MMCrossingMinimizationModule.py generated from classogdf_1_1_m_m_crossing_minimization_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMCrossingMinimizationModule(ogdf.Module):

	"""Interface for minor-monotone crossing minimization algorithms."""

	def __init__(self) -> None:
		"""Initializes a minor-monotone crossing minimization module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, splittableNodes : List[node], cr : int, forbid : EdgeArray[ bool ] = None) -> ReturnType:
		"""Performs minor-monotone crossing minimization onGfor given splittable nodes."""
		...

	@overload
	def call(self, G : Graph, cr : int, forbid : EdgeArray[ bool ] = None) -> ReturnType:
		"""Performs minor-monotone crossing minimization onG."""
		...

	@overload
	def call(self, PG : PlanRepExpansion, cc : int, crossingNumber : int, forbid : EdgeArray[ bool ] = None) -> ReturnType:
		"""Computes a planarized representation of an expansion of the input graph."""
		...

	def numberOfNodeSplits(self) -> int:
		"""Returns the number of required node splits after the call."""
		...

	def numberOfSplittedNodes(self) -> int:
		...

	def doCall(self, PG : PlanRepExpansion, cc : int, forbid : EdgeArray[ bool ], crossingNumber : int, numNS : int, numSN : int) -> ReturnType:
		"""Actual algorithm call that needs to be implemented by derived classed."""
		...
