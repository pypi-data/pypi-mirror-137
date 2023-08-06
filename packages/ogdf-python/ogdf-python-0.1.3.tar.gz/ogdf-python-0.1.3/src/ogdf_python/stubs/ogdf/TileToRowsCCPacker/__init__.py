# file stubs/ogdf/TileToRowsCCPacker/__init__.py generated from classogdf_1_1_tile_to_rows_c_c_packer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TileToRowsCCPacker(ogdf.CCLayoutPackModule):

	"""The tile-to-rows algorithm for packing drawings of connected components."""

	def __init__(self) -> None:
		"""Creates an instance of tile-to-rows packer."""
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
