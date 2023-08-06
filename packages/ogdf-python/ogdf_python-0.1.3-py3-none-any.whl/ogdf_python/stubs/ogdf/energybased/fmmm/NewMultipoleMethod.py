# file stubs/ogdf/energybased/fmmm/NewMultipoleMethod.py generated from classogdf_1_1energybased_1_1fmmm_1_1_new_multipole_method
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NewMultipoleMethod(object):

	# Functions needed for path by path tree construction @{

	# Functions needed for subtree by subtree tree construction

	def __init__(self) -> None:
		"""Constructor."""
		...

	def calculate_repulsive_forces(self, G : Graph, A : NodeArray[NodeAttributes], F_rep : NodeArray[DPoint]) -> None:
		"""Calculate rep. forces for each node."""
		...

	def deallocate_memory(self) -> None:
		"""Dynamically allocated memory is freed here."""
		...

	def make_initialisations(self, G : Graph, boxlength : float, down_left_corner : DPoint, particles_in_leaves : int, precision : int, tree_construction_way : FMMMOptions.ReducedTreeConstruction, find_small_cell : FMMMOptions.SmallestCellFinding) -> None:
		"""Make all initialisations that are needed for New Multipole Method (NMM)"""
		...

	def update_boxlength_and_cornercoordinate(self, b_l : float, d_l_c : DPoint) -> None:
		"""Import updated information of the drawing area."""
		...
