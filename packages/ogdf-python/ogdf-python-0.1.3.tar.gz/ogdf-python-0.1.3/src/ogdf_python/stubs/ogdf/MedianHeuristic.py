# file stubs/ogdf/MedianHeuristic.py generated from classogdf_1_1_median_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MedianHeuristic(ogdf.LayerByLayerSweep):

	"""The median heuristic for 2-layer crossing minimization."""

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the median heuristic."""
		...

	@overload
	def __init__(self, crossMin : MedianHeuristic) -> None:
		"""Creates a new instance of the median heuristic."""
		...

	def call(self, L : Level) -> None:
		"""Calls the median heuristic for levelL."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the median heuristic with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes crossing minimization for hierarchyH."""
		...
