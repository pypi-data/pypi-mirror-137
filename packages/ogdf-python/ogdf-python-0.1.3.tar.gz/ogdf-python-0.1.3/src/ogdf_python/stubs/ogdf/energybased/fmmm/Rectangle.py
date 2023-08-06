# file stubs/ogdf/energybased/fmmm/Rectangle.py generated from classogdf_1_1energybased_1_1fmmm_1_1_rectangle
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Rectangle(object):

	"""Helping data structure for packing rectangles; The width, height and the position of the down left corner of the tight surroundig rectangle is represented for each connected component of the graph."""

	def __init__(self) -> None:
		...

	def get_component_index(self) -> int:
		...

	def get_height(self) -> float:
		...

	def get_new_dlc_position(self) -> DPoint:
		...

	def get_old_dlc_position(self) -> DPoint:
		...

	def get_width(self) -> float:
		...

	def is_tipped_over(self) -> bool:
		...

	def set_component_index(self, comp_index : int) -> None:
		...

	def set_height(self, h : float) -> None:
		...

	def set_new_dlc_position(self, dlc_pos : DPoint) -> None:
		...

	def set_old_dlc_position(self, dlc_pos : DPoint) -> None:
		...

	def set_rectangle(self, w : float, h : float, old_dlc_x_pos : float, old_dlc_y_pos : float, comp_index : int) -> None:
		...

	def set_width(self, w : float) -> None:
		...

	def tipp_over(self) -> None:
		...
