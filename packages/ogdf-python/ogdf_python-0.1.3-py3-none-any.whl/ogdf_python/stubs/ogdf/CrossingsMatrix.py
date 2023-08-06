# file stubs/ogdf/CrossingsMatrix.py generated from classogdf_1_1_crossings_matrix
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingsMatrix(object):

	"""Implements crossings matrix which is used by some TwoLayerCrossingMinimization heuristics (e.g. split)"""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, levels : HierarchyLevels) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def init(self, L : Level) -> None:
		"""ordinary init"""
		...

	@overload
	def init(self, L : Level, edgeSubGraphs : EdgeArray[  int ]) -> None:
		"""SimDrawinit."""
		...

	def __call__(self, i : int, j : int) -> int:
		...

	def swap(self, i : int, j : int) -> None:
		...
