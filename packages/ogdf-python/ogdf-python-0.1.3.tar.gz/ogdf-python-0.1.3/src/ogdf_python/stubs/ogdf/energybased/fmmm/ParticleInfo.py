# file stubs/ogdf/energybased/fmmm/ParticleInfo.py generated from classogdf_1_1energybased_1_1fmmm_1_1_particle_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ParticleInfo(object):

	"""Helping data structure for building up the reduced quad tree by NMM."""

	def __init__(self) -> None:
		"""constructor"""
		...

	def get_copy_item(self) -> ListIterator[ParticleInfo]:
		...

	def get_cross_ref_item(self) -> ListIterator[ParticleInfo]:
		...

	def get_subList_ptr(self) -> List[ParticleInfo]:
		...

	def get_tmp_cross_ref_item(self) -> ListIterator[ParticleInfo]:
		...

	def get_vertex(self) -> node:
		...

	def get_x_y_coord(self) -> float:
		...

	def is_marked(self) -> bool:
		...

	def mark(self) -> None:
		...

	def set_copy_item(self, it : ListIterator[ParticleInfo]) -> None:
		...

	def set_cross_ref_item(self, it : ListIterator[ParticleInfo]) -> None:
		...

	def set_subList_ptr(self, ptr : List[ParticleInfo]) -> None:
		...

	def set_tmp_cross_ref_item(self, it : ListIterator[ParticleInfo]) -> None:
		...

	def set_vertex(self, v : node) -> None:
		...

	def set_x_y_coord(self, c : float) -> None:
		...

	def unmark(self) -> None:
		...
