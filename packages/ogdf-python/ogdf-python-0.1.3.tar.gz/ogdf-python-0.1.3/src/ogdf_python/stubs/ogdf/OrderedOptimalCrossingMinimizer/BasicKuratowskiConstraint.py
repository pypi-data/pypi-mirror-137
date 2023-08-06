# file stubs/ogdf/OrderedOptimalCrossingMinimizer/BasicKuratowskiConstraint.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_basic_kuratowski_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BasicKuratowskiConstraint(ogdf.OrderedOptimalCrossingMinimizer.KuratowskiConstraintBase):

	newCrossings : Array[Array[edge] ] = ...

	oldCrossings : Array[CrossingVariableBase] = ...

	@overload
	def __init__(self, m : abacus.Master, K : KuratowskiSubdivision, dynamic : bool, rness : Restrictiveness = 0) -> None:
		...

	@overload
	def __init__(self, b : BasicKuratowskiConstraint) -> None:
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

	def equals(self, ki : BasicKuratowskiConstraint) -> bool:
		...

	def hashKey(self) -> None:
		"""Should provide a key for the constraint/variable that can be used to insert it into a hash table."""
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
