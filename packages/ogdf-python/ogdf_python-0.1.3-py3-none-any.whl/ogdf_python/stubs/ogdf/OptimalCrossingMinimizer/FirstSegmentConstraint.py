# file stubs/ogdf/OptimalCrossingMinimizer/FirstSegmentConstraint.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_first_segment_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FirstSegmentConstraint(ogdf.OptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, t : edge) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...

	def referenceEdge(self) -> edge:
		...
