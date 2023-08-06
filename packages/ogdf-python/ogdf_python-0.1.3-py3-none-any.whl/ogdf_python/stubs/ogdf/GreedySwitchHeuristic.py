# file stubs/ogdf/GreedySwitchHeuristic.py generated from classogdf_1_1_greedy_switch_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GreedySwitchHeuristic(ogdf.LayerByLayerSweep):

	"""The greedy-switch heuristic for 2-layer crossing minimization."""

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the greedy-switch heuristic."""
		...

	@overload
	def __init__(self, crossMin : GreedySwitchHeuristic) -> None:
		"""Creates a new instance of the greedy-switch heuristic."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, L : Level) -> None:
		"""Calls the greedy switch heuristic for levelL."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the greed-switch heuristic with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes crossing minimization for hierarchyH."""
		...
