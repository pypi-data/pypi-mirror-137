# file stubs/ogdf/SplitHeuristic.py generated from classogdf_1_1_split_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SplitHeuristic(ogdf.TwoLayerCrossMinSimDraw):

	"""The split heuristic for 2-layer crossing minimization."""

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the split heuristic."""
		...

	@overload
	def __init__(self, crossMin : SplitHeuristic) -> None:
		"""Creates a new instance of the split heuristic."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, L : Level) -> None:
		"""Calls the split heuristic for levelL."""
		...

	@overload
	def call(self, L : Level, edgeSubGraphs : EdgeArray[  int ]) -> None:
		"""Calls the median heuristic for levelL(simultaneous drawing)."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> TwoLayerCrossMinSimDraw:
		"""Returns a new instance of the splitheurisitc with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes crossing minimization for hierarchyH."""
		...
