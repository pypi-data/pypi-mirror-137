# file stubs/ogdf/OrthoGridLayout.py generated from classogdf_1_1_ortho_grid_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoGridLayout(ogdf.GridLayoutPlanRepModule):

	"""Represents planar orthogonal grid drawing algorithm."""

	def __init__(self) -> None:
		...

	def getOptions(self) -> int:
		...

	@overload
	def margin(self) -> float:
		"""Get the distance from the tight bounding box to the boundary of the drawing."""
		...

	@overload
	def margin(self, m : int) -> None:
		...

	def optionProfile(self, i : int) -> None:
		"""Set the option profile, thereby fixing a set of drawing options."""
		...

	def setBendBound(self, i : int) -> None:
		"""Set bound on the number of bends."""
		...

	def setconstructiveCompactor(self, ocm : OrthoCompactionModule) -> None:
		...

	def setEmbedder(self, pEmbedder : EmbedderModule) -> None:
		"""Sets the module option for the graph embedding algorithm."""
		...

	def setImprovementCompactor(self, ocm : OrthoCompactionModule) -> None:
		...

	def setOptions(self, optionField : int) -> None:
		...

	def classifyEdges(self, PG : PlanRepUML, adjExternal : adjEntry) -> None:
		...

	def doCall(self, PG : PlanRep, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool = False) -> None:
		"""Implements the algorithm call."""
		...
