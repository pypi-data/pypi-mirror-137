# file stubs/ogdf/OrderedOptimalCrossingMinimizer/KnSubdivConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_kn_subdiv_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KnSubdivConstraint(ogdf.OrderedOptimalCrossingMinimizer.KuratowskiConstraintBase):

	@overload
	def __init__(self, b : KnSubdivConstraint) -> None:
		...

	@overload
	def __init__(self, m : OrderedOptimalCrossingMinimizer.Master, tReplace : edge, tVia : node, dynamic : bool, rness : Restrictiveness = 0, local : bool = False) -> None:
		...

	def clone(self) -> KuratowskiConstraintBase:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def equal(self, cv : abacus.ConVar) -> bool:
		"""Should compare if the constraint/variable is identical (in a mathematical sense) with the constraint/variablecv."""
		...

	def equalConst(self, cv : KuratowskiConstraintBase) -> bool:
		...

	def equals(self, ki : KnSubdivConstraint) -> bool:
		...

	def hashKey(self) -> None:
		"""Should provide a key for the constraint/variable that can be used to insert it into a hash table."""
		...
