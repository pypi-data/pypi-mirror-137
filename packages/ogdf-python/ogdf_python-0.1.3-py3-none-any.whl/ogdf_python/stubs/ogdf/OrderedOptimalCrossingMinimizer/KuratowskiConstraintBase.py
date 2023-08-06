# file stubs/ogdf/OrderedOptimalCrossingMinimizer/KuratowskiConstraintBase.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_kuratowski_constraint_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KuratowskiConstraintBase(ogdf.OrderedOptimalCrossingMinimizer.AbacusConstraint, ogdf.Logger):

	KuratowskiType : Type = int

	Restrictiveness : Type = int

	type : KuratowskiType = ...

	KT_K33 : KuratowskiType = ...

	KT_K5 : KuratowskiType = ...

	@overload
	def allTypeToCr(self, kt : KuratowskiType) -> int:
		...

	@overload
	def crossingApplicable(self, kt : KuratowskiType, p1 : int, p2 : int) -> bool:
		...

	def KTBipartite(self, n : int, m : int) -> KuratowskiType:
		...

	def KTComplete(self, n : int) -> KuratowskiType:
		...

	def REqualPlus(self, i : int) -> Restrictiveness:
		...

	def RGreaterPlus(self, i : int) -> Restrictiveness:
		...

	def RPlus(self, r : Restrictiveness) -> int:
		...

	def RSense(self, r : Restrictiveness) -> abacus.CSense.SENSE:
		...

	def subdivision2type(self, K : KuratowskiSubdivision) -> KuratowskiType:
		...

	@overload
	def typeToCr(self, kt : KuratowskiType) -> int:
		...

	@overload
	def typeToPaths(self, kt : KuratowskiType) -> int:
		...

	@overload
	def __init__(self, m : abacus.Master, t : KuratowskiType, dynamic : bool, rness : Restrictiveness = 0, local : bool = False) -> None:
		...

	@overload
	def __init__(self, k : KuratowskiConstraintBase) -> None:
		...

	@overload
	def allTypeToCr(self) -> int:
		...

	def branchMe(self, S : Subproblem, k1 : KuratowskiConstraintBase, k2 : KuratowskiConstraintBase) -> None:
		...

	def clone(self) -> KuratowskiConstraintBase:
		...

	@overload
	def crossingApplicable(self, p1 : int, p2 : int) -> bool:
		...

	def equalConst(self, cv : KuratowskiConstraintBase) -> bool:
		...

	def isCompleteOdd(self) -> bool:
		...

	@overload
	def typeToCr(self) -> int:
		...

	@overload
	def typeToPaths(self) -> int:
		...
