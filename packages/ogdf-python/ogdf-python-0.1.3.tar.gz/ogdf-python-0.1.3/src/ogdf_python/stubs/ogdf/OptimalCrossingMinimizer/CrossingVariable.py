# file stubs/ogdf/OptimalCrossingMinimizer/CrossingVariable.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_crossing_variable
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingVariable(ogdf.OptimalCrossingMinimizer.CrossingLocation, abacus.Variable):

	def __init__(self, m : abacus.Master, seg1 : Segment, seg2 : Segment) -> None:
		...

	@overload
	def correspondsTo(self, s : Segment) -> bool:
		...

	@overload
	def correspondsTo(self, e : edge) -> bool:
		...

	@overload
	def correspondsTo(self, e : edge, num : int) -> bool:
		...

	@overload
	def correspondsTo(self, n : node) -> bool:
		...
