# file stubs/ogdf/OrthoLayoutUML.py generated from classogdf_1_1_ortho_layout_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoLayoutUML(ogdf.LayoutPlanRepUMLModule):

	"""Represents planar orthogonal drawing algorithm for mixed-upward planar embedded graphs (UML-diagrams)"""

	def __init__(self) -> None:
		...

	def align(self, b : bool) -> None:
		"""Set alignment option."""
		...

	def call(self, PG : PlanRepUML, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Computes a planar layout ofPGindrawing."""
		...

	@overload
	def costAssoc(self) -> int:
		...

	@overload
	def costAssoc(self, c : int) -> None:
		...

	@overload
	def costGen(self) -> int:
		...

	@overload
	def costGen(self, c : int) -> None:
		...

	@overload
	def cOverhang(self) -> float:
		...

	@overload
	def cOverhang(self, c : float) -> None:
		...

	def getOptions(self) -> int:
		"""Returns the (generic) options."""
		...

	@overload
	def margin(self) -> float:
		...

	@overload
	def margin(self, m : float) -> None:
		...

	def optionProfile(self, i : int) -> None:
		"""Set the option profile, thereby fixing a set of drawing options."""
		...

	@overload
	def preferedDir(self) -> OrthoDir:
		...

	@overload
	def preferedDir(self, dir : OrthoDir) -> None:
		...

	def scaling(self, b : bool) -> None:
		"""Set scaling compaction."""
		...

	@overload
	def separation(self) -> float:
		"""Returns the minimal allowed distance between edges and vertices."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimal allowed distance between edges and vertices tosep."""
		...

	def setBendBound(self, i : int) -> None:
		"""Set bound on the number of bends."""
		...

	def setOptions(self, _ : int) -> None:
		"""Sets the (generic) options; derived classes have to cope with the interpretation)"""
		...

	def classifyEdges(self, PG : PlanRepUML, adjExternal : adjEntry) -> None:
		...
