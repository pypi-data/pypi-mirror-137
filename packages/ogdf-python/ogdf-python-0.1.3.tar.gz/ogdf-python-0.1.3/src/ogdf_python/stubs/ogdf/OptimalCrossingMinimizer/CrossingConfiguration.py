# file stubs/ogdf/OptimalCrossingMinimizer/CrossingConfiguration.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_crossing_configuration
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingConfiguration(object):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, PG : PlanRep, crNo : int, direct : bool) -> None:
		...

	def getCrossingEdges(self, e : edge) -> List[edge]:
		...

	def getCrossingNo(self) -> int:
		...

	def initDirect(self, PG : PlanRep, crNo : int) -> None:
		...

	def initIndirect(self, PG : PlanRep, crNo : int) -> None:
		...
