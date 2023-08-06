# file stubs/ogdf/UpwardPlanarizerModule.py generated from classogdf_1_1_upward_planarizer_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanarizerModule(ogdf.Module):

	"""Interface for upward planarization algorithms."""

	def __init__(self) -> None:
		"""Initializes an upward planarizer module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, UPR : UpwardPlanRep, cost : EdgeArray[  int ] = None, forbid : EdgeArray[ bool ] = None) -> ReturnType:
		"""Computes a upward planarized representation (UPR) of the input graphG."""
		...

	def __call__(self, UPR : UpwardPlanRep, cost : EdgeArray[  int ] = None, forbid : EdgeArray[ bool ] = None) -> ReturnType:
		"""Computes a upward planarized representation of the input graph (shorthand for call)"""
		...

	def useCost(self) -> bool:
		"""Returns true iff edge costs are given."""
		...

	def useForbid(self) -> bool:
		"""Returns true iff forbidden edges are given."""
		...

	def doCall(self, UPR : UpwardPlanRep, cost : EdgeArray[  int ], forbid : EdgeArray[ bool ]) -> ReturnType:
		"""Computes an upward planarized representation of the input graph."""
		...
