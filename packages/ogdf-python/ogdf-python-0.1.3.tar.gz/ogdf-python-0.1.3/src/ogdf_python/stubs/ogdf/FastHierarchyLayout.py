# file stubs/ogdf/FastHierarchyLayout.py generated from classogdf_1_1_fast_hierarchy_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FastHierarchyLayout(ogdf.HierarchyLayoutModule):

	"""Coordinate assignment phase for the Sugiyama algorithm by Buchheim et al."""

	def doCall(self, levels : HierarchyLevelsBase, AGC : GraphAttributes) -> None:
		"""Implements the actual algorithm call."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of fast hierarchy layout."""
		...

	@overload
	def __init__(self, _ : FastHierarchyLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def fixedLayerDistance(self) -> bool:
		"""Returns the optionfixed layer distance."""
		...

	@overload
	def fixedLayerDistance(self, b : bool) -> None:
		"""Sets the option fixed layer distance tob."""
		...

	@overload
	def layerDistance(self) -> float:
		"""Returns the optionlayer distance."""
		...

	@overload
	def layerDistance(self, dist : float) -> None:
		"""Sets the option layer distance todist."""
		...

	@overload
	def nodeDistance(self) -> float:
		"""Returns the optionnode distance."""
		...

	@overload
	def nodeDistance(self, dist : float) -> None:
		"""Sets the option node distance todist."""
		...

	def __assign__(self, _ : FastHierarchyLayout) -> FastHierarchyLayout:
		"""Assignment operator."""
		...
