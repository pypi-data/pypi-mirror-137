# file stubs/ogdf/CCLayoutPackModule.py generated from classogdf_1_1_c_c_layout_pack_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CCLayoutPackModule(object):

	"""Base class of algorithms that arrange/pack layouts of connected components."""

	def __init__(self) -> None:
		"""Initializes a layout packing module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, box : Array[DPoint], offset : Array[DPoint], pageRatio : float = 1.0) -> None:
		"""Arranges the rectangles given bybox."""
		...

	@overload
	def call(self, box : Array[IPoint], offset : Array[IPoint], pageRatio : float = 1.0) -> None:
		"""Arranges the rectangles given bybox."""
		...

	@overload
	def __call__(self, box : Array[DPoint], offset : Array[DPoint], pageRatio : float = 1.0) -> None:
		"""Arranges the rectangles given bybox."""
		...

	@overload
	def __call__(self, box : Array[IPoint], offset : Array[IPoint], pageRatio : float = 1.0) -> None:
		"""Arranges the rectangles given bybox."""
		...

	@overload
	def checkOffsets(self, box : Array[DPoint], offset : Array[DPoint]) -> bool:
		"""Checks if the rectangles inboxdo not overlap for given offsets."""
		...

	@overload
	def checkOffsets(self, box : Array[IPoint], offset : Array[IPoint]) -> bool:
		"""Checks if the rectangles inboxdo not overlap for given offsets."""
		...
