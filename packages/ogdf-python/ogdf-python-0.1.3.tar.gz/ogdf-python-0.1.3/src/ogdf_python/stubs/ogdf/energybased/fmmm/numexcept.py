# file stubs/ogdf/energybased/fmmm/numexcept.py generated from classogdf_1_1energybased_1_1fmmm_1_1numexcept
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class numexcept(object):

	"""This class is developed for exceptions that might occure, when nodes are placed at the same position and a new random position has to be found, or when the calculated forces are near the machine accuracy, where no reasonable numeric and logic calculations are possible any more."""

	def choose_distinct_random_point_in_disque(self, old_point : DPoint, xmin : float, xmax : float, ymin : float, ymax : float) -> DPoint:
		"""Returns a distinct random point within the smallest disque D with center old_point that is contained in the box defined by xmin,...,ymax; The size of D is shrunk by multiplying with epsilon = 0.1; Precondition: old_point is contained in the box and the box is not equal to old_point."""
		...

	def f_near_machine_precision(self, distance : float, force : DPoint) -> bool:
		"""If distance has a value near the machine precision the (attractive)force calculation is not possible (calculated values exceed the machine accuracy) in this cases true is returned and force is set to a reasonable value that does not cause problems; Else false is returned and force keeps unchanged."""
		...

	def f_rep_u_on_v(self, pos_u : DPoint, pos_v : DPoint) -> DPoint:
		...

	def nearly_equal(self, a : float, b : float) -> bool:
		"""Returns true if a is "nearly" equal to b (needed, when machine accuracy is insufficient in functions well_seperated and bordering of NMM)"""
		...

	def choose_distinct_random_point_in_radius_epsilon(self, old_pos : DPoint) -> DPoint:
		"""A random point (distinct from old_pos) on the disque around old_pos with radius epsilon = 0.1 is computed."""
		...

	def f_rep_near_machine_precision(self, distance : float, force : DPoint) -> bool:
		"""If distance has a value near the machine precision the repulsive force calculation is not possible (calculated values exceed the machine accuracy) in this cases true is returned and force is set to a reasonable value that does not cause problems; Else false is returned and force keeps unchanged."""
		...

	def f_rep_scalar(self, d : float) -> float:
		"""Returns the repulsing force_function_value of scalar d."""
		...
