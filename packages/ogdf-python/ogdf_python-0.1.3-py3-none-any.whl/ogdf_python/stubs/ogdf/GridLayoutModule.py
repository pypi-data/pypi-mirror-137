# file stubs/ogdf/GridLayoutModule.py generated from classogdf_1_1_grid_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridLayoutModule(ogdf.LayoutModule):

	"""Base class for grid layout algorithms."""

	#: The computed bounding box of the grid layout.
	m_gridBoundingBox : IPoint = ...

	def __init__(self) -> None:
		"""Initializes a grid layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the grid layout algorithm (general call)."""
		...

	def callGrid(self, G : Graph, gridLayout : GridLayout) -> None:
		"""Calls the grid layout algorithm (call forGridLayout)."""
		...

	def gridBoundingBox(self) -> IPoint:
		...

	@overload
	def separation(self) -> float:
		"""Returns the current setting of the minimum distance between nodes."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimum distance between nodes."""
		...

	def doCall(self, G : Graph, gridLayout : GridLayout, boundingBox : IPoint) -> None:
		"""Implements the algorithm call."""
		...
