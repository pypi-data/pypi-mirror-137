# file stubs/ogdf/energybased/fmmm/EdgeAttributes.py generated from classogdf_1_1energybased_1_1fmmm_1_1_edge_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeAttributes(object):

	"""helping data structure that stores the graphical attributes of an edge that are needed for the force-directed algorithms."""

	# for the divide et impera step in FMMM @{

	def set_original_edge(self, e : edge) -> None:
		...

	def set_subgraph_edge(self, e : edge) -> None:
		...

	def get_original_edge(self) -> edge:
		...

	def get_subgraph_edge(self) -> edge:
		...

	# for the preprocessing step in FMMM (set/get_original_edge are needed, too) @{

	def set_copy_edge(self, e : edge) -> None:
		...

	def get_copy_edge(self) -> edge:
		...

	# for multilevel step @{

	def set_higher_level_edge(self, e : edge) -> None:
		...

	def get_higher_level_edge(self) -> edge:
		...

	def is_moon_edge(self) -> bool:
		...

	def make_moon_edge(self) -> None:
		...

	def is_extra_edge(self) -> bool:
		...

	def make_extra_edge(self) -> None:
		...

	def mark_as_normal_edge(self) -> None:
		...

	def init_mult_values(self) -> None:
		...

	def __init__(self) -> None:
		"""Constructor."""
		...

	def get_length(self) -> float:
		...

	def set_EdgeAttributes(self, len : float, e_orig : edge, e_sub : edge) -> None:
		...

	def set_length(self, len : float) -> None:
		...
