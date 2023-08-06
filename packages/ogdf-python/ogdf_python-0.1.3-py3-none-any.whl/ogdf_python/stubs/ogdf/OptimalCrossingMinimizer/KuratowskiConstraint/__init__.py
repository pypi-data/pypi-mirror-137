# file stubs/ogdf/OptimalCrossingMinimizer/KuratowskiConstraint/__init__.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_kuratowski_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KuratowskiConstraint(ogdf.OptimalCrossingMinimizer.AbacusConstraint, ogdf.Logger):

	KuratowskiType : Type = int

	Restrictiveness : Type = int

	KT_K33 : KuratowskiType = ...

	KT_K5 : KuratowskiType = ...

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

	def typeToCr(self, kt : KuratowskiType) -> int:
		...

	@overload
	def __init__(self, m : abacus.Master, S : Subproblem, R : GraphReduction, K : KuratowskiSubdivision, dynamic : bool, rness : int = 0, local : bool = False) -> None:
		...

	@overload
	def __init__(self, m : abacus.Master, ltype : KuratowskiType, dynamic : bool, rness : int = 0, local : bool = False) -> None:
		...

	@overload
	def __init__(self, orig : KuratowskiConstraint) -> None:
		...

	def __destruct__(self) -> None:
		...

	def adapt(self, varidx : int, newvar : CrossingVariable, e : edge, oldi : int, newi : int) -> None:
		...

	def addAccordingCrossing(self, S : Subproblem, I : PlanRep, e : edge, eid : int, L : List[CrossingLocation]) -> None:
		...

	def addEdge(self, e : edge, path : int) -> None:
		...

	def addSegments(self, e : edge, path : int, start : int, end : int) -> None:
		...

	def branchMe(self, S : Subproblem, k1 : KuratowskiConstraint, k2 : KuratowskiConstraint) -> None:
		...

	def build(self, S : Subproblem, R : GraphReduction, K : KuratowskiSubdivision) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def equal(self, cv : abacus.ConVar) -> bool:
		"""Should compare if the constraint/variable is identical (in a mathematical sense) with the constraint/variablecv."""
		...

	def equals(self, ki : KuratowskiConstraint) -> bool:
		...

	def getEdges(self) -> EdgeArray[SegmentRange]:
		...

	def getRequiredCrossings(self) -> Array[CrossingLocation]:
		...

	def getType(self) -> KuratowskiType:
		...

	def hashKey(self) -> None:
		"""Should provide a key for the constraint/variable that can be used to insert it into a hash table."""
		...

	def isCompleteOdd(self) -> bool:
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
