# file stubs/ogdf/MaximalFUPS.py generated from classogdf_1_1_maximal_f_u_p_s
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MaximalFUPS(ogdf.FUPSModule):

	def __init__(self) -> None:
		...

	def getTimelimit(self) -> int:
		...

	def setTimelimit(self, timelimit : int) -> None:
		...

	def doCall(self, UPR : UpwardPlanRep, delEdges : List[edge]) -> Module.ReturnType:
		"""Computes a feasible upward planar subgraph of the input graph."""
		...
