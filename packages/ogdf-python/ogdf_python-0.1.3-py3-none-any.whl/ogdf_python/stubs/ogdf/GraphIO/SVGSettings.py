# file stubs/ogdf/GraphIO/SVGSettings.py generated from classogdf_1_1_graph_i_o_1_1_s_v_g_settings
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SVGSettings(object):

	"""Condensed settings for drawing SVGs."""

	def __init__(self) -> None:
		...

	@overload
	def bezierInterpolation(self) -> bool:
		"""Returns whether Bézier-interpolation for curved edges is enabled."""
		...

	@overload
	def bezierInterpolation(self, enable : bool) -> None:
		"""Enables or disables Bézier-interpolation."""
		...

	@overload
	def curviness(self) -> float:
		"""Returns the curviness of the edges (value ranges from 0 to 1)."""
		...

	@overload
	def curviness(self, value : float) -> None:
		"""Sets the curviness of all edges (value ranges from 0 to 1)."""
		...

	@overload
	def fontColor(self) -> str:
		"""Returns the default font color."""
		...

	@overload
	def fontColor(self, fc : str) -> None:
		"""Sets the default font color tofc."""
		...

	@overload
	def fontFamily(self) -> str:
		"""Returns the default font family."""
		...

	@overload
	def fontFamily(self, fm : str) -> None:
		"""Sets the default font family tofm."""
		...

	@overload
	def fontSize(self) -> int:
		"""Returns the default font size (font height in pixels)."""
		...

	@overload
	def fontSize(self, fs : int) -> None:
		"""Sets the default font size (font height in pixels) tofs."""
		...

	@overload
	def height(self) -> str:
		"""Returns the default height."""
		...

	@overload
	def height(self, height : str) -> None:
		"""Sets the height."""
		...

	@overload
	def margin(self) -> float:
		"""Returns the size of the margin around the drawing."""
		...

	@overload
	def margin(self, m : float) -> None:
		"""Sets the size of the margin around the drawing tom."""
		...

	@overload
	def width(self) -> str:
		"""Returns the default width."""
		...

	@overload
	def width(self, width : str) -> None:
		"""Sets the width."""
		...
