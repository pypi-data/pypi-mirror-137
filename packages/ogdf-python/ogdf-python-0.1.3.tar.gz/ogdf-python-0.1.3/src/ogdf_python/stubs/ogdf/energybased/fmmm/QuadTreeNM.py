# file stubs/ogdf/energybased/fmmm/QuadTreeNM.py generated from classogdf_1_1energybased_1_1fmmm_1_1_quad_tree_n_m
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class QuadTreeNM(object):

	"""Helping data structure that stores the information needed to represent the modified quadtree in the New Multipole Method (NMM)"""

	def __init__(self) -> None:
		"""Constructor."""
		...

	@overload
	def cout_preorder(self, node_ptr : QuadTreeNodeNM) -> None:
		"""Pre_order traversal of the tree rooted at node_ptr (with or without output of the M,L-lists from 0 to precision)."""
		...

	@overload
	def cout_preorder(self, node_ptr : QuadTreeNodeNM, precision : int) -> None:
		...

	@overload
	def create_new_lb_child(self) -> None:
		...

	@overload
	def create_new_lb_child(self, L_x_ptr : List[ParticleInfo], L_y_ptr : List[ParticleInfo]) -> None:
		"""Creates a new left_bottom_child of the actual node (importing L_x(y)_ptr)."""
		...

	@overload
	def create_new_lt_child(self) -> None:
		...

	@overload
	def create_new_lt_child(self, L_x_ptr : List[ParticleInfo], L_y_ptr : List[ParticleInfo]) -> None:
		"""Creates a new left_top_child of the actual node (importing L_x(y)_ptr)."""
		...

	@overload
	def create_new_rb_child(self) -> None:
		...

	@overload
	def create_new_rb_child(self, L_x_ptr : List[ParticleInfo], L_y_ptr : List[ParticleInfo]) -> None:
		"""Creates a new right_bottom_child of the actual node(importing L_x(y)_ptr)."""
		...

	@overload
	def create_new_rt_child(self) -> None:
		...

	@overload
	def create_new_rt_child(self, L_x_ptr : List[ParticleInfo], L_y_ptr : List[ParticleInfo]) -> None:
		"""Creates a new right_top_child of the actual node (importing L_x(y)_ptr)."""
		...

	def delete_tree(self, node_ptr : QuadTreeNodeNM) -> None:
		"""Deletes the tree starting at node_ptr."""
		...

	def delete_tree_and_count_nodes(self, node_ptr : QuadTreeNodeNM, nodecounter : int) -> None:
		"""Deletes the tree starting at node_ptr and counts the nodes of the subtree."""
		...

	def get_act_ptr(self) -> QuadTreeNodeNM:
		"""Returns the actual/root node pointer of the tree."""
		...

	def get_root_ptr(self) -> QuadTreeNodeNM:
		...

	def go_to_father(self) -> None:
		"""Sets act_ptr to the father_ptr."""
		...

	def go_to_lb_child(self) -> None:
		"""Sets act_ptr to the left_bottom_child_ptr."""
		...

	def go_to_lt_child(self) -> None:
		"""Sets act_ptr to the left_top_child_ptr."""
		...

	def go_to_rb_child(self) -> None:
		"""Sets act_ptr to the right_bottom_child_ptr."""
		...

	def go_to_rt_child(self) -> None:
		"""Sets act_ptr to the right_top_child_ptr."""
		...

	def init_tree(self) -> None:
		"""Creates the root node and lets act_ptr and root_ptr point to the root node."""
		...

	def set_act_ptr(self, a_ptr : QuadTreeNodeNM) -> None:
		"""Sets act_ptr to a_ptr."""
		...

	def set_root_node(self, r : QuadTreeNodeNM) -> None:
		"""Sets the content of *root_ptr to r."""
		...

	def set_root_ptr(self, r_ptr : QuadTreeNodeNM) -> None:
		"""Sets root_ptr to r_ptr."""
		...

	def start_at_root(self) -> None:
		"""Sets act_ptr to the root_ptr."""
		...
