# file stubs/ogdf/OrderedOptimalCrossingMinimizer/CrossingConfiguration.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_crossing_configuration
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingConfiguration(object):

	@overload
	def __init__(self, G : Graph) -> None:
		...

	@overload
	def __init__(self, PG : PlanRep, crNo : int, direct : bool) -> None:
		...

	def extractDirect(self, PG : PlanRep, crNo : int) -> None:
		...

	def extractIndirect(self, PG : PlanRep, crNo : int) -> None:
		...

	def getCrossingEdges(self, e : edge) -> List[edge]:
		...

	def getCrossingNo(self) -> int:
		...

	def paste(self, PG : PlanRep) -> None:
		...

	def probablyExchangeCrossingEdges(self, e : edge, newList : List[edge]) -> bool:
		...

	def targetCrossingEdge(self, PR : PlanRep, x : edge) -> edge:
		...

	def targetSuccEdge(self, PR : PlanRep, x : edge) -> edge:
		...
