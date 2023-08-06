# file stubs/ogdf/CircularLayout.py generated from classogdf_1_1_circular_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CircularLayout(ogdf.LayoutModule):

	"""The circular layout algorithm."""

	# The algorithm call

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a circular layout for graph attributesGA."""
		...

	# Optional parameters

	@overload
	def minDistCircle(self) -> float:
		"""Returns the optionminDistCircle."""
		...

	@overload
	def minDistCircle(self, x : float) -> None:
		"""Sets the optionminDistCircletox."""
		...

	@overload
	def minDistLevel(self) -> float:
		"""Returns the optionminDistLevel."""
		...

	@overload
	def minDistLevel(self, x : float) -> None:
		"""Sets the optionminDistLeveltox."""
		...

	@overload
	def minDistSibling(self) -> float:
		"""Returns the optionminDistSibling."""
		...

	@overload
	def minDistSibling(self, x : float) -> None:
		"""Sets the optionminDistSiblingtox."""
		...

	@overload
	def minDistCC(self) -> float:
		"""Returns the optionminDistCC."""
		...

	@overload
	def minDistCC(self, x : float) -> None:
		"""Sets the optionminDistCCtox."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the optionpageRatio."""
		...

	@overload
	def pageRatio(self, x : float) -> None:
		"""Sets the optionpageRatiotox."""
		...

	def __init__(self) -> None:
		"""Creates an instance of circular layout."""
		...

	def __destruct__(self) -> None:
		...
