# file stubs/ogdf/TutteLayout.py generated from classogdf_1_1_tutte_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TutteLayout(ogdf.LayoutModule):

	"""Tutte's layout algorithm."""

	def __init__(self) -> None:
		...

	@overload
	def bbox(self) -> DRect:
		...

	@overload
	def bbox(self, bb : DRect) -> None:
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	@overload
	def call(self, AG : GraphAttributes, givenNodes : List[node]) -> None:
		...
