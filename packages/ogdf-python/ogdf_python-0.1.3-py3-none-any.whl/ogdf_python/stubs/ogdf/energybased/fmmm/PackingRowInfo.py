# file stubs/ogdf/energybased/fmmm/PackingRowInfo.py generated from classogdf_1_1energybased_1_1fmmm_1_1_packing_row_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PackingRowInfo(object):

	"""Helping data structure forMAARPacking."""

	def __init__(self) -> None:
		...

	def get_max_height(self) -> float:
		...

	def get_row_index(self) -> int:
		...

	def get_total_width(self) -> float:
		...

	def set_max_height(self, h : float) -> None:
		...

	def set_row_index(self, i : int) -> None:
		...

	def set_total_width(self, w : float) -> None:
		...
