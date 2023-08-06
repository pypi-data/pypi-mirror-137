# file stubs/ogdf/MMCBBase.py generated from classogdf_1_1_m_m_c_b_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MMCBBase(ogdf.MixedModelCrossingsBeautifierModule):

	"""common base class forMMCBDoubleGridandMMCBLocalStretch."""

	def __init__(self) -> None:
		"""Constructor (does nothing)."""
		...

	def __destruct__(self) -> None:
		...

	def copyOn(self, old_a : int, new_a : int) -> None:
		...

	def insertBend(self, gl : GridLayout, e : edge, v : node, x : int, y : int) -> None:
		...

	def workOn(self, gl : GridLayout, v : node) -> int:
		...
