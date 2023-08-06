# file stubs/ogdf/BarycenterHeuristic.py generated from classogdf_1_1_barycenter_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BarycenterHeuristic(ogdf.LayerByLayerSweep):

	"""The barycenter heuristic for 2-layer crossing minimization."""

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the barycenter heuristic."""
		...

	@overload
	def __init__(self, crossMin : BarycenterHeuristic) -> None:
		"""Creates a new instance of the barycenter heuristic."""
		...

	def call(self, L : Level) -> None:
		"""Calls the barycenter heuristic for levelL."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the barycenter heuristic with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes crossing minimization for hierarchyH."""
		...
