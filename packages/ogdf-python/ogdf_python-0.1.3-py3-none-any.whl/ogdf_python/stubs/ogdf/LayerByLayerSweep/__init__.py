# file stubs/ogdf/LayerByLayerSweep/__init__.py generated from classogdf_1_1_layer_by_layer_sweep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayerByLayerSweep(ogdf.LayeredCrossMinModule):

	"""Interface of two-layer crossing minimization algorithms."""

	def __init__(self) -> None:
		"""Initializes a two-layer crossing minimization module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, L : Level) -> None:
		"""Performs crossing minimization for levelL."""
		...

	def cleanup(self) -> None:
		"""Performs clean-up."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the two-layer crossing minimization module with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes the crossing minimization module for hierarchy levelslevels."""
		...

	def __call__(self, L : Level) -> None:
		"""Performs crossing minimization for levelL."""
		...

	@overload
	def reduceCrossings(self, sugi : SugiyamaLayout, H : Hierarchy, nCrossings : int) -> HierarchyLevels:
		...

	@overload
	def reduceCrossings(self, sugi : SugiyamaLayout, H : Hierarchy, nCrossings : int) -> HierarchyLevels:
		"""Template method implementation of reduceCrossings fromLayeredCrossMinModule."""
		...
