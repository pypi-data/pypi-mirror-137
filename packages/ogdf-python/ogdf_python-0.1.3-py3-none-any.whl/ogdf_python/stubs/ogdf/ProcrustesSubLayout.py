# file stubs/ogdf/ProcrustesSubLayout.py generated from classogdf_1_1_procrustes_sub_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ProcrustesSubLayout(ogdf.LayoutModule):

	"""Simple procrustes analysis."""

	def __init__(self, pSubLayout : LayoutModule) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def scaleToInitialLayout(self) -> bool:
		"""Should the new layout scale be used or the initial scale? Defaults totrue."""
		...

	def setScaleToInitialLayout(self, flag : bool) -> None:
		"""Should the new layout scale be used or the initial scale? Defaults totrue."""
		...
