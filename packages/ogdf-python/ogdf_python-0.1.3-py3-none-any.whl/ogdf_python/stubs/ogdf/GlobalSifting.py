# file stubs/ogdf/GlobalSifting.py generated from classogdf_1_1_global_sifting
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GlobalSifting(ogdf.LayeredCrossMinModule):

	"""The global sifting heuristic for crossing minimization."""

	@overload
	def nRepeats(self) -> int:
		"""Returns the current setting of option nRepeats."""
		...

	@overload
	def nRepeats(self, num : int) -> None:
		"""Sets the option nRepeats tonum."""
		...

	def reduceCrossings(self, sugi : SugiyamaLayout, H : Hierarchy, nCrossings : int) -> HierarchyLevelsBase:
		"""Implementation of interface LateredCrossMinModule."""
		...
