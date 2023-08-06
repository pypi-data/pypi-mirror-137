# file stubs/ogdf/UpSAT/__init__.py generated from classogdf_1_1_up_s_a_t
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpSAT(object):

	@overload
	def __init__(self, G : Graph) -> None:
		...

	@overload
	def __init__(self, G : GraphCopy, feasibleOriginalEdges : bool) -> None:
		...

	def embedUpwardPlanar(self, externalToItsRight : adjEntry, nodeOrder : NodeArray[  int ] = None) -> bool:
		...

	def getNumberOfClauses(self) -> int:
		...

	def getNumberOfVariables(self) -> int:
		...

	def reset(self) -> None:
		...

	def testUpwardPlanarity(self, nodeOrder : NodeArray[  int ] = None) -> bool:
		...
