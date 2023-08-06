# file stubs/ogdf/PlanarGridLayoutModule.py generated from classogdf_1_1_planar_grid_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarGridLayoutModule(ogdf.GridLayoutModule):

	"""Base class for planar grid layout algorithms."""

	def __init__(self) -> None:
		"""Initializes a planar grid layout module."""
		...

	def __destruct__(self) -> None:
		...

	def callFixEmbed(self, AG : GraphAttributes, adjExternal : adjEntry = None) -> None:
		"""Calls the grid layout algorithm with a fixed planar embedding (general call)."""
		...

	def callGridFixEmbed(self, G : Graph, gridLayout : GridLayout, adjExternal : adjEntry = None) -> None:
		"""Calls the grid layout algorithm with a fixed planar embedding (call forGridLayout)."""
		...

	@overload
	def doCall(self, G : Graph, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""Implements the algorithm call."""
		...

	@overload
	def doCall(self, G : Graph, gridLayout : GridLayout, boundingBox : IPoint) -> None:
		"""Implements theGridLayoutModule::doCall()."""
		...

	def handleTrivial(self, G : Graph, gridLayout : GridLayout, boundingBox : IPoint) -> bool:
		"""Handles the special cases of graphs with less than 3 nodes."""
		...
