# file stubs/ogdf/PivotMDS.py generated from classogdf_1_1_pivot_m_d_s
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PivotMDS(ogdf.LayoutModule):

	"""The Pivot MDS (multi-dimensional scaling) layout algorithm."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graph attributesGA."""
		...

	def setEdgeCosts(self, edgeCosts : float) -> None:
		"""Sets the desired distance between adjacent nodes. If the new value is smaller or equal 0 the default value (100) is used."""
		...

	def setNumberOfPivots(self, numberOfPivots : int) -> None:
		"""Sets the number of pivots. If the new value is smaller or equal 0 the default value (250) is used."""
		...

	@overload
	def useEdgeCostsAttribute(self) -> bool:
		...

	@overload
	def useEdgeCostsAttribute(self, useEdgeCostsAttribute : bool) -> None:
		...
