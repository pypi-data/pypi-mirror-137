# file stubs/ogdf/PlanRepLight.py generated from classogdf_1_1_plan_rep_light
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanRepLight(ogdf.GraphCopy):

	"""Light-weight version of a planarized representation, associated with aPlanRep."""

	def __init__(self, pr : PlanRep) -> None:
		"""Creates a light-weight planarized representation."""
		...

	def ccInfo(self) -> CCsInfo:
		"""Returns the connected component info structure."""
		...

	def currentCC(self) -> int:
		"""Returns the index of the current connected component."""
		...

	def e(self, i : int) -> edge:
		"""Returns the original edge with indexi."""
		...

	def initCC(self, cc : int) -> None:
		"""Initializes the planarized representation for connected componentcc."""
		...

	def numberOfCCs(self) -> int:
		"""Returns the number of connected components in the original graph."""
		...

	def startEdge(self) -> int:
		"""Returns the index of the first edge in this connected component."""
		...

	def stopEdge(self) -> int:
		"""Returns the index of (one past) the last edge in this connected component."""
		...

	def typeOf(self, e : edge) -> EdgeType:
		...

	def typeOrig(self, eOrig : edge) -> EdgeType:
		...

	def v(self, i : int) -> node:
		"""Returns the original node with indexi."""
		...
