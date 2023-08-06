# file stubs/ogdf/HierarchyLayoutModule.py generated from classogdf_1_1_hierarchy_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HierarchyLayoutModule(object):

	"""Interface of hierarchy layout algorithms."""

	def __init__(self) -> None:
		"""Initializes a hierarchy layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, levels : HierarchyLevelsBase, GA : GraphAttributes) -> None:
		"""Computes a hierarchy layout oflevelsinGA."""
		...

	def dynLayerDistance(self, AGC : GraphAttributes, levels : HierarchyLevelsBase) -> None:
		...

	def getHeight(self, GA : GraphAttributes, levels : HierarchyLevelsBase, v : node) -> float:
		"""Returns theGAheight of nodevor 0 if it is a dummy node in the hierarchy oflevels."""
		...

	def getWidth(self, GA : GraphAttributes, levels : HierarchyLevelsBase, v : node) -> float:
		"""Returns theGAwidth of nodevor 0 if it is a dummy node in the hierarchy oflevels."""
		...

	def doCall(self, levels : HierarchyLevelsBase, AGC : GraphAttributes) -> None:
		"""Implements the actual algorithm call."""
		...
