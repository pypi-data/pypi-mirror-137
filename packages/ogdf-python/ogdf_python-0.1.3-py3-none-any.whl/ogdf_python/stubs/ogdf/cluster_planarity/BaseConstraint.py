# file stubs/ogdf/cluster_planarity/BaseConstraint.py generated from classogdf_1_1cluster__planarity_1_1_base_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BaseConstraint(abacus.Constraint):

	"""Basic constraint type."""

	def __init__(self, master : abacus.Master, sub : abacus.Sub, sense : abacus.CSense.SENSE, rhs : float, dynamic : bool, local : bool, liftable : bool) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	@overload
	def coeff(self, n : NodePair) -> int:
		...
