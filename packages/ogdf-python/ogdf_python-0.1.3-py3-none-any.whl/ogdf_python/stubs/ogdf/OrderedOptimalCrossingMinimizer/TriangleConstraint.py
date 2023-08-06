# file stubs/ogdf/OrderedOptimalCrossingMinimizer/TriangleConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_triangle_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TriangleConstraint(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, _base : edge, _tri : node, _crossedBy : edge, _before : edge) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def equal(self, cv : abacus.ConVar) -> bool:
		"""Should compare if the constraint/variable is identical (in a mathematical sense) with the constraint/variablecv."""
		...

	def equals(self, tc : TriangleConstraint) -> bool:
		...

	def hashKey(self) -> None:
		"""Should provide a key for the constraint/variable that can be used to insert it into a hash table."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
