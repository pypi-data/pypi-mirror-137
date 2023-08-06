# file stubs/ogdf/FUPSSimple.py generated from classogdf_1_1_f_u_p_s_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FUPSSimple(ogdf.FUPSModule):

	def __init__(self) -> None:
		"""Creates an instance of feasible subgraph algorithm."""
		...

	def __destruct__(self) -> None:
		...

	def getAdjEntry(self, Gamma : CombinatorialEmbedding, v : node, f : face) -> adjEntry:
		"""return a adjEntry of node v which right face is f. Be Carefully! The adjEntry is not always unique."""
		...

	@overload
	def runs(self) -> int:
		"""Returns the current number of randomized runs."""
		...

	@overload
	def runs(self, nRuns : int) -> None:
		"""Sets the number of randomized runs tonRuns."""
		...

	def doCall(self, UPR : UpwardPlanRep, delEdges : List[edge]) -> Module.ReturnType:
		"""Computes a feasible upward planar subgraph of the input graph."""
		...
