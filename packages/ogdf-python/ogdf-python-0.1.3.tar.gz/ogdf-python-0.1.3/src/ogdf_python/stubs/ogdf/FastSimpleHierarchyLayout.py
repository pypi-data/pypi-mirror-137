# file stubs/ogdf/FastSimpleHierarchyLayout.py generated from classogdf_1_1_fast_simple_hierarchy_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FastSimpleHierarchyLayout(ogdf.HierarchyLayoutModule):

	"""Coordinate assignment phase for the Sugiyama algorithm by Ulrik Brandes and Boris Köpf."""

	def doCall(self, levels : HierarchyLevelsBase, AGC : GraphAttributes) -> None:
		"""Implements the actual algorithm call."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of fast simple hierarchy layout."""
		...

	@overload
	def __init__(self, _ : FastSimpleHierarchyLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def balanced(self) -> bool:
		"""Returns the optionbalanced."""
		...

	@overload
	def balanced(self, b : bool) -> None:
		"""Sets the optionbalancedtob."""
		...

	@overload
	def downward(self) -> bool:
		"""Returns the optiondownward."""
		...

	@overload
	def downward(self, d : bool) -> None:
		"""Sets the optiondownwardtod."""
		...

	@overload
	def layerDistance(self) -> float:
		"""Returns the optionlayer distance."""
		...

	@overload
	def layerDistance(self, dist : float) -> None:
		"""Sets the optionlayer distancetodist."""
		...

	@overload
	def leftToRight(self) -> bool:
		"""Returns the optionleft-to-right."""
		...

	@overload
	def leftToRight(self, b : bool) -> None:
		"""Sets the optionleft-to-righttob."""
		...

	@overload
	def nodeDistance(self) -> float:
		"""Returns the optionnode distance."""
		...

	@overload
	def nodeDistance(self, dist : float) -> None:
		"""Sets the option node distance todist."""
		...

	def __assign__(self, _ : FastSimpleHierarchyLayout) -> FastSimpleHierarchyLayout:
		"""Assignment operator."""
		...
