# file stubs/ogdf/HananiTutteCPlanarity/CLinearSystem/__init__.py generated from classogdf_1_1_hanani_tutte_c_planarity_1_1_c_linear_system
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CLinearSystem(object):

	ObjectTable : Type = Dict[Object,  int ]

	def __init__(self) -> None:
		...

	def addTrivialEquation(self) -> int:
		...

	def clear(self) -> None:
		...

	def equation(self, numc : int) -> GF2Solver.Equation:
		...

	def numberOfColumns(self) -> int:
		...

	def numberOfConditions(self) -> int:
		...

	def numberOfMoves(self) -> int:
		...

	def numberOfRows(self) -> int:
		...

	def numCond(self, eo1 : Object, eo2 : Object) -> int:
		...

	def numeomove(self, eo : Object, obj : Object) -> int:
		...

	def numOx(self, obj : Object) -> int:
		...

	def objects(self) -> Dict[Object,  int ]:
		...

	def pairs(self) -> Dict[  int, std.pair[Object,Object] ]:
		...

	def solve(self) -> bool:
		...
