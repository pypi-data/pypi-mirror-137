# file stubs/ogdf/GreedyInsertHeuristic.py generated from classogdf_1_1_greedy_insert_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GreedyInsertHeuristic(ogdf.LayerByLayerSweep):

	"""The greedy-insert heuristic for 2-layer crossing minimization."""

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the greedy-insert heuristic."""
		...

	@overload
	def __init__(self, crossMin : GreedyInsertHeuristic) -> None:
		"""Creates a new instance of the greedy-insert heuristic."""
		...

	def call(self, L : Level) -> None:
		"""Calls the greedy insert heuristic for levelL."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the greed-insert heuristic with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes weights and crossing minimization for hierarchyH."""
		...
