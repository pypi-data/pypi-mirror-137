# file stubs/ogdf/LinearLayout.py generated from classogdf_1_1_linear_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LinearLayout(ogdf.LayoutModule):

	"""Layout the graph with nodes next to each other with natural or custom order and draw the edges as semicircular bows above them."""

	@overload
	def __init__(self) -> None:
		"""Constructor that uses a standard width and no custom order of the nodes."""
		...

	@overload
	def __init__(self, w : float, o : ListPure[node]) -> None:
		"""Constructor that takes a desired width and a custom ordering."""
		...

	def __destruct__(self) -> None:
		"""Standard destructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def setCustomOrder(self, o : bool) -> None:
		"""Interface function to toggle custom ordering."""
		...
