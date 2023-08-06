# file stubs/ogdf/OrderedOptimalCrossingMinimizer/ctwoEdge.py generated from structogdf_1_1_ordered_optimal_crossing_minimizer_1_1ctwo_edge
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ctwoEdge(object):

	x : edge = ...

	@overload
	def __init__(self, y : ctwoEdge) -> None:
		...

	@overload
	def __init__(self, y0 : edge, y1 : edge) -> None:
		...

	@overload
	def __getitem__(self, i : int) -> edge:
		...

	@overload
	def __getitem__(self, i : int) -> edge:
		...
