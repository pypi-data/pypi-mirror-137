# file stubs/ogdf/davidson_harel/UniformGrid.py generated from classogdf_1_1davidson__harel_1_1_uniform_grid
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UniformGrid(object):

	@overload
	def __init__(self, _ : GraphAttributes) -> None:
		...

	@overload
	def __init__(self, _ : GraphAttributes, node, _ : DPoint) -> None:
		...

	@overload
	def __init__(self, _ : UniformGrid, node, _ : DPoint) -> None:
		...

	def newGridNecessary(self, v : node, p : DPoint) -> bool:
		...

	def numberOfCrossings(self) -> int:
		...
