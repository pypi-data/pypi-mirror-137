# file stubs/ogdf/LayeredCrossMinModule.py generated from classogdf_1_1_layered_cross_min_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayeredCrossMinModule(object):

	"""Interface of crossing minimization algorithms for layered graphs."""

	def __init__(self) -> None:
		"""Creates empty module."""
		...

	def __destruct__(self) -> None:
		"""Destruct."""
		...

	def cleanup(self) -> None:
		"""Performs clean-up."""
		...

	def reduceCrossings(self, sugi : SugiyamaLayout, H : Hierarchy, nCrossings : int) -> HierarchyLevelsBase:
		"""Calls the actual crossing minimization algorithm."""
		...
