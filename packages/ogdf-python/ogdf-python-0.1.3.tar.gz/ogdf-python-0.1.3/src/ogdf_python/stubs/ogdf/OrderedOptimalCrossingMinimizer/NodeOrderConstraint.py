# file stubs/ogdf/OrderedOptimalCrossingMinimizer/NodeOrderConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_node_order_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeOrderConstraint(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint):

	def __init__(self, m : abacus.Master, tn1 : node, tn2 : node) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
