# file stubs/ogdf/OptimalCrossingMinimizer/SegmentOrderConstraint.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_segment_order_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SegmentOrderConstraint(ogdf.OptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, t : Segment) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
