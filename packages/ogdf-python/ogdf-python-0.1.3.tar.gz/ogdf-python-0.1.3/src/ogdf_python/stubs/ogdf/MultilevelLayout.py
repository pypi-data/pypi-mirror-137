# file stubs/ogdf/MultilevelLayout.py generated from classogdf_1_1_multilevel_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MultilevelLayout(ogdf.LayoutModule):

	"""The multilevel drawing framework."""

	def __init__(self) -> None:
		"""Constructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calculates a drawing for theGraphGA."""
		...

	def setLayout(self, L : LayoutModule) -> None:
		"""Sets the single level layout."""
		...

	def setMultilevelBuilder(self, B : MultilevelBuilder) -> None:
		"""Sets the method used for coarsening."""
		...

	def setPlacer(self, P : InitialPlacer) -> None:
		"""Sets the placement method used when refining the levels again."""
		...
