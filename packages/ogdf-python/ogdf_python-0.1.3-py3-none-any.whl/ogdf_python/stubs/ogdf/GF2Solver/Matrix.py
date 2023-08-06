# file stubs/ogdf/GF2Solver/Matrix.py generated from classogdf_1_1_g_f2_solver_1_1_matrix
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Matrix(object):

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def addColumn(self) -> int:
		...

	def addRow(self) -> int:
		...

	def clear(self) -> None:
		...

	def numColumns(self) -> int:
		...

	def numRows(self) -> int:
		...

	@overload
	def __getitem__(self, i : int) -> Equation:
		...

	@overload
	def __getitem__(self, i : int) -> Equation:
		...

	def print(self) -> None:
		...
