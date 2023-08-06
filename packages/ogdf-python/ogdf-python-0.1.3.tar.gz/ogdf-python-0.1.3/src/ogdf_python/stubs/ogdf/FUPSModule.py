# file stubs/ogdf/FUPSModule.py generated from classogdf_1_1_f_u_p_s_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FUPSModule(ogdf.Module):

	"""Interface for feasible upward planar subgraph algorithms."""

	def __init__(self) -> None:
		"""Initializes a feasible upward planar subgraph module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, UPR : UpwardPlanRep, delEdges : List[edge]) -> ReturnType:
		"""Computes a feasible upward planar subgraph of the input graph."""
		...

	def __call__(self, UPR : UpwardPlanRep, delEdges : List[edge]) -> ReturnType:
		"""Computes a upward planarized representation of the input graph (shorthand for call)"""
		...

	def doCall(self, UPR : UpwardPlanRep, delEdges : List[edge]) -> ReturnType:
		"""Computes a feasible upward planar subgraph of the input graph."""
		...
