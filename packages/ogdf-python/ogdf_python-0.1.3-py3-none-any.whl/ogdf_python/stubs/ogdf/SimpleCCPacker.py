# file stubs/ogdf/SimpleCCPacker.py generated from classogdf_1_1_simple_c_c_packer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimpleCCPacker(ogdf.LayoutModule):

	"""Splits and packs the components of aGraph."""

	m_bottomMargin : float = ...

	m_leftMargin : float = ...

	m_pSubLayoutModule : std.unique_ptr[LayoutModule] = ...

	m_rightMargin : float = ...

	m_topMargin : float = ...

	def __init__(self, pSubLayoutModule : LayoutModule = None) -> None:
		"""Constructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def setMargins(self, left : float, top : float, right : float, bottom : float) -> None:
		...

	def computeBoundingBox(self, graphAttributes : GraphAttributes, min_coord : DPoint, max_coord : DPoint) -> None:
		...
