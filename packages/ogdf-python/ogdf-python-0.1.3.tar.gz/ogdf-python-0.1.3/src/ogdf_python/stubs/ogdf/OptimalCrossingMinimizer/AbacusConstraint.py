# file stubs/ogdf/OptimalCrossingMinimizer/AbacusConstraint.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_abacus_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AbacusConstraint(abacus.Constraint):

	@overload
	def __init__(self, master : abacus.Master, sub : abacus.Sub, sense : abacus.CSense.SENSE, rhs : float, dynamic : bool, local : bool, liftable : bool) -> None:
		...

	@overload
	def __init__(self, c : AbacusConstraint) -> None:
		...

	def master(self) -> OptimalCrossingMinimizer.Master:
		...
