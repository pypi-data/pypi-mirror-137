# file stubs/ogdf/SetYCoords.py generated from classogdf_1_1_set_y_coords
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SetYCoords(object):

	def __init__(self, G : Graph, iops : IOPoints, mmo : MMOrder, x : NodeArray[  int ], y : NodeArray[  int ]) -> None:
		...

	@overload
	def checkYCoord(self, xleft : int, xright : int, ys : int, nodeSep : bool) -> None:
		...

	@overload
	def checkYCoord(self, xs : int, ys : int, nodeSep : bool) -> None:
		...

	def getYmax(self) -> int:
		...

	def init(self, k : int) -> None:
		...

	def __assign__(self, _ : SetYCoords) -> SetYCoords:
		...
