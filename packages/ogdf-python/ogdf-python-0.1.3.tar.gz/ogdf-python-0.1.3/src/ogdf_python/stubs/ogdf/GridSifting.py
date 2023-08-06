# file stubs/ogdf/GridSifting.py generated from classogdf_1_1_grid_sifting
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridSifting(ogdf.LayeredCrossMinModule):

	"""The grid sifting heuristic for crossing minimization."""

	def reduceCrossings(self, sugi : SugiyamaLayout, H : Hierarchy, nCrossings : int) -> HierarchyLevelsBase:
		"""Calls the actual crossing minimization algorithm."""
		...

	@overload
	def verticalStepsBound(self) -> int:
		"""Returns the current setting of option verticalStepsBound."""
		...

	@overload
	def verticalStepsBound(self, b : int) -> None:
		"""Sets the option verticalStepsBound tob."""
		...
