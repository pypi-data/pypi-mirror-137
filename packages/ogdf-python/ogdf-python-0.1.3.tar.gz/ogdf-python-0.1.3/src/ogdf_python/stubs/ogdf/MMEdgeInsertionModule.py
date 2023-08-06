# file stubs/ogdf/MMEdgeInsertionModule.py generated from classogdf_1_1_m_m_edge_insertion_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMEdgeInsertionModule(ogdf.Module):

	"""Interface for minor-monotone edge insertion algorithms."""

	def __init__(self) -> None:
		"""Initializes a minor-monotone edge insertion module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, PG : PlanRepExpansion, origEdges : List[edge]) -> ReturnType:
		"""Inserts all edges inorigEdgesintoPG."""
		...

	@overload
	def call(self, PG : PlanRepExpansion, origEdges : List[edge], forbiddenEdgeOrig : EdgeArray[ bool ]) -> ReturnType:
		"""Inserts all edges inorigEdgesintoPGand forbids crossingforbiddenEdges."""
		...

	def doCall(self, PG : PlanRepExpansion, origEdges : List[edge], forbiddenEdgeOrig : EdgeArray[ bool ]) -> ReturnType:
		"""Actual algorithm call that has to be implemented by derived classes."""
		...
