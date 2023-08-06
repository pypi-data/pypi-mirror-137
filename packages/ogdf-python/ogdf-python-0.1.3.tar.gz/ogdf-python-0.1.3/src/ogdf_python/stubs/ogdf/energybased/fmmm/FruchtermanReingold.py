# file stubs/ogdf/energybased/fmmm/FruchtermanReingold.py generated from classogdf_1_1energybased_1_1fmmm_1_1_fruchterman_reingold
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FruchtermanReingold(object):

	def __init__(self) -> None:
		"""Constructor."""
		...

	def calculate_approx_repulsive_forces(self, G : Graph, A : NodeArray[NodeAttributes], F_rep : NodeArray[DPoint]) -> None:
		"""Grid approximation of rep.forces for each node."""
		...

	def calculate_exact_repulsive_forces(self, G : Graph, A : NodeArray[NodeAttributes], F_rep : NodeArray[DPoint]) -> None:
		"""Calculate exact rep. forces for each node."""
		...

	def make_initialisations(self, boxlength : float, down_left_corner : DPoint, grid_quotient : int) -> None:
		"""Make all initialisations that are needed forFruchtermanReingold."""
		...

	def update_boxlength_and_cornercoordinate(self, b_l : float, d_l_c : DPoint) -> None:
		"""Import updated information of the drawing area."""
		...
