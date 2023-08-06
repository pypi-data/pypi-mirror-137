# file stubs/ogdf/energybased/fmmm/NodeAttributes.py generated from classogdf_1_1energybased_1_1fmmm_1_1_node_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeAttributes(object):

	"""helping data structure that stores the graphical attributes of a node that are needed for the force-directed algorithms."""

	# for preprocessing step in FMMM @{

	def set_original_node(self, v : node) -> None:
		...

	def set_copy_node(self, v : node) -> None:
		...

	def get_original_node(self) -> node:
		...

	def get_copy_node(self) -> node:
		...

	# for divide et impera step in FMMM (set/get_original_node() are needed, too) @{

	def set_subgraph_node(self, v : node) -> None:
		...

	def get_subgraph_node(self) -> node:
		...

	# for the multilevel step in FMMM @{

	def set_lower_level_node(self, v : node) -> None:
		...

	def set_higher_level_node(self, v : node) -> None:
		...

	def get_lower_level_node(self) -> node:
		...

	def get_higher_level_node(self) -> node:
		...

	def set_mass(self, m : int) -> None:
		...

	def set_type(self, t : int) -> None:
		...

	def set_dedicated_sun_node(self, v : node) -> None:
		...

	def set_dedicated_sun_distance(self, d : float) -> None:
		...

	def set_dedicated_pm_node(self, v : node) -> None:
		...

	def place(self) -> None:
		...

	def set_angle_1(self, a : float) -> None:
		...

	def set_angle_2(self, a : float) -> None:
		...

	# for the multilevel and divide et impera and preprocessing step @{

	# for the multilevel step @{

	def __init__(self) -> None:
		"""Constructor."""
		...

	def get_angle_1(self) -> float:
		...

	def get_angle_2(self) -> float:
		...

	def get_dedicated_moon_node_List_ptr(self) -> List[node]:
		...

	def get_dedicated_pm_node(self) -> node:
		...

	def get_dedicated_sun_distance(self) -> float:
		...

	def get_dedicated_sun_node(self) -> node:
		...

	def get_height(self) -> float:
		...

	def get_lambda_List_ptr(self) -> List[ float ]:
		...

	def get_mass(self) -> int:
		...

	def get_neighbour_sun_node_List_ptr(self) -> List[node]:
		...

	def get_position(self) -> DPoint:
		...

	def get_type(self) -> int:
		...

	def get_width(self) -> float:
		...

	def get_x(self) -> float:
		...

	def get_y(self) -> float:
		...

	def init_mult_values(self) -> None:
		"""initialzes all values needed for multilevel representations"""
		...

	def is_placed(self) -> bool:
		...

	def set_height(self, h : float) -> None:
		...

	def set_NodeAttributes(self, w : float, h : float, pos : DPoint, v_low : node, v_high : node) -> None:
		...

	def set_position(self, pos : DPoint) -> None:
		...

	def set_width(self, w : float) -> None:
		...

	def set_x(self, x : float) -> None:
		...

	def set_y(self, y : float) -> None:
		...
