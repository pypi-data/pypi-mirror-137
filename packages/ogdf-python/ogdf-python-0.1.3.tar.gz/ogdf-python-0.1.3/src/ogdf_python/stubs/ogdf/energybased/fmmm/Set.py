# file stubs/ogdf/energybased/fmmm/Set.py generated from classogdf_1_1energybased_1_1fmmm_1_1_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Comp = TypeVar('Comp')

class Set(object):

	"""Helping data structure that holds set S_node of nodes in the range [0, G.number_of_nodes()-1] (needed for classMultilevel) for randomly choosing nodes (with uniform or weighted probability!)"""

	# for set of nodes @{

	@overload
	def init_node_set(self, G : Graph) -> None:
		"""Inits S_node[0,...,G.number_of_nodes()-1] and stores the i-th node of P at position S_node[i] and in position_in_node_set for each node its index in S_node."""
		...

	def empty_node_set(self) -> bool:
		"""Returns whether S_node is empty or not."""
		...

	def is_deleted(self, v : node) -> bool:
		"""Returns true if and only if v is deleted from S_node."""
		...

	def delete_node(self, v : node) -> None:
		"""Deletes the node v from S_node."""
		...

	# for set of nodes with uniform probability @{

	def get_random_node(self) -> node:
		"""Selects a random element from S_node with uniform probability and updates S_node and position_in_node_set."""
		...

	# for set of nodes with weighted  probability @{

	@overload
	def init_node_set(self, G : Graph, A : NodeArray[NodeAttributes]) -> None:
		"""Same as init_node_set(G), but additionally the array mass_of_star is caculated."""
		...

	# for set of nodes with `&lsquo;lower mass&rsquo;' probability @{

	def get_random_node_with_lowest_star_mass(self, rand_tries : int) -> node:
		"""Gets rand_tries random elements from S_node and selects the one with the lowest mass_of_star and updates S_node and position_in_node_set."""
		...

	# for set of nodes with `&lsquo;higher mass&rsquo;' probability @{

	def get_random_node_with_highest_star_mass(self, rand_tries : int) -> node:
		"""Gets rand_tries random elements from S_node and selects the one with the highest mass_of_star and updates S_node and position_in_node_set."""
		...

	def __init__(self) -> None:
		"""constructor"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def set_seed(self, rand_seed : int) -> None:
		"""the the random seed to rand_seed"""
		...

	def get_random_node_common(self, _ : int, _ : int) -> node:
		"""Common updates for each get_random_node method."""
		...

	def get_random_node_with_some_star_mass(self, rand_tries : int, comp : Comp = Comp()) -> node:
		"""Helper function for get_random_node methods with lowest or highest star mass."""
		...
