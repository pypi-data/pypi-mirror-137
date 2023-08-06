# file stubs/ogdf/OptimalCrossingMinimizer/Master/__init__.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Master(ogdf.optimal_crossing_minimizer.MasterBase):

	constCrossingLocationComparer : ConstCrossingLocationComparer = ...

	lastIntegerCrossings : List[CrossingLocation] = ...

	lastRoundedCrossings : List[CrossingLocation] = ...

	def __init__(self) -> None:
		...

	def enumerationStrategy(self, s1 : abacus.Sub, s2 : abacus.Sub) -> int:
		"""Analyzes the enumeration strategy set in the parameter file.abacusand calls the corresponding comparison function for the subproblemss1ands2."""
		...

	def equalCrossingLists(self, L1 : List[CrossingLocation], integerList : bool) -> bool:
		...

	def firstSub(self) -> abacus.Sub:
		"""Should return a pointer to the first subproblem of the optimization, i.e., the root node of the enumeration tree."""
		...

	def getExpansionFactor(self) -> int:
		...

	@overload
	def hintEffects(self) -> int:
		...

	@overload
	def hintEffects(self, h : int) -> None:
		...

	def initializeOptimization(self) -> None:
		"""The default implementation ofinitializeOptimization()does nothing."""
		...

	def doCall(self, PG : PlanRep, cc : int, cost : EdgeArray[  int ], forbid : EdgeArray[ bool ], subgraphs : EdgeArray[  int ], crossingNumber : int) -> ReturnType:
		...

	def doWriteBestSolution(self) -> None:
		...

	def helperHintsKnAllSubKuratowskis(self, aktnodes : NodeArray[ bool ], posNode : node, num : int, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnAllSubKuratowskis(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnEdgeOrder(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnExpensiveKuratowski(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnKuratowskiMinusOne(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnmAllSubKuratowskis(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnmEdgeOrder(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnmKuratowskiMinusOne(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnmNodeOrder(self, prelist : List[abacus.Constraint]) -> None:
		...

	def hintsKnNodeOrder(self, prelist : List[abacus.Constraint]) -> None:
		...
