# file stubs/ogdf/OrderedOptimalCrossingMinimizer/CyclicOrderConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_cyclic_order_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CyclicOrderConstraint(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, _e : edge, _f : edge, _g : edge, _h : edge) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...

	def print(self, out : std.ostream) -> None:
		"""Writes the constraint/variable to the output streamout."""
		...
