# file stubs/ogdf/OrderedOptimalCrossingMinimizer/ToroidalSubgridConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_toroidal_subgrid_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ToroidalSubgridConstraint(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, tf : int, tn : int, tdiv : bool, trhs : int) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def isRemoved(self, e : edge) -> bool:
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
