# file stubs/ogdf/OrderedOptimalCrossingMinimizer/HypercubeConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_hypercube_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypercubeConstraint(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, tbit : int, isset : bool, trhs : int) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
