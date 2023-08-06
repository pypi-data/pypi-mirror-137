# file stubs/ogdf/OptimalCrossingMinimizer/ConstCrossingLocationComparer.py generated from classogdf_1_1_optimal_crossing_minimizer_1_1_const_crossing_location_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ConstCrossingLocationComparer(object):

	ConstCrossingLocationPointer : Type = CrossingLocation

	def compare(self, x : ConstCrossingLocationPointer, y : ConstCrossingLocationPointer) -> int:
		...
