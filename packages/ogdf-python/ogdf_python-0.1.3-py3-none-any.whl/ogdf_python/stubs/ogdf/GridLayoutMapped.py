# file stubs/ogdf/GridLayoutMapped.py generated from classogdf_1_1_grid_layout_mapped
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridLayoutMapped(ogdf.GridLayout):

	"""ExtendsGridLayoutby a grid mapping mechanism."""

	def __init__(self, PG : PlanRep, OR : OrthoRep, separation : float, cOverhang : float, fineness : int = 4) -> None:
		...

	@overload
	def height(self) -> NodeArray[  int ]:
		...

	@overload
	def height(self) -> NodeArray[  int ]:
		...

	@overload
	def height(self, v : node) -> int:
		...

	@overload
	def height(self, v : node) -> int:
		...

	def remap(self, drawing : Layout) -> None:
		"""Transforms the grid layout to a layout."""
		...

	def toDouble(self, i : int) -> float:
		...

	def toGrid(self, x : float) -> int:
		...

	@overload
	def width(self) -> NodeArray[  int ]:
		...

	@overload
	def width(self) -> NodeArray[  int ]:
		...

	@overload
	def width(self, v : node) -> int:
		...

	@overload
	def width(self, v : node) -> int:
		...
