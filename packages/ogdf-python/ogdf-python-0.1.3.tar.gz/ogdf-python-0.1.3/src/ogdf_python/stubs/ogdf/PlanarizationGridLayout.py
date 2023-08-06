# file stubs/ogdf/PlanarizationGridLayout.py generated from classogdf_1_1_planarization_grid_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarizationGridLayout(ogdf.GridLayoutModule):

	"""The planarization grid layout algorithm."""

	# Optional parameters

	@overload
	def pageRatio(self) -> float:
		"""Returns the current setting of option pageRatio."""
		...

	@overload
	def pageRatio(self, ratio : float) -> None:
		"""Sets the option pageRatio toratio."""
		...

	# Module options

	def setCrossMin(self, pCrossMin : CrossingMinimizationModule) -> None:
		"""Sets the module option for crossing minimization."""
		...

	def setPlanarLayouter(self, pPlanarLayouter : GridLayoutPlanRepModule) -> None:
		"""Sets the module option for the planar grid layout algorithm."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components."""
		...

	# Further information

	def numberOfCrossings(self) -> int:
		"""Returns the number of crossings in computed layout."""
		...

	def __init__(self) -> None:
		"""Creates an instance of planarization layout and sets options to default values."""
		...

	def __destruct__(self) -> None:
		...

	def doCall(self, G : Graph, gridLayout : GridLayout, boundingBox : IPoint) -> None:
		"""Implements the algorithm call."""
		...
