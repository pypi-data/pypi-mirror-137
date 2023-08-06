# file stubs/ogdf/embedder/CrossingStructure.py generated from classogdf_1_1embedder_1_1_crossing_structure
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingStructure(object):

	def __init__(self) -> None:
		...

	def crossings(self, e : edge) -> SListPure[  int ]:
		...

	def init(self, PG : PlanRepLight, weightedCrossingNumber : int) -> None:
		...

	def numberOfCrossings(self) -> int:
		...

	def restore(self, PG : PlanRep, cc : int) -> None:
		...

	def weightedCrossingNumber(self) -> int:
		...
