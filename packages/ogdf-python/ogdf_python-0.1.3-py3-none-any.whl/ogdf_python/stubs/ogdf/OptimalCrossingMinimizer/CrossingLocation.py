# file stubs/ogdf/OptimalCrossingMinimizer/CrossingLocation.py generated from structogdf_1_1_optimal_crossing_minimizer_1_1_crossing_location
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingLocation(object):

	s1 : Segment = ...

	s2 : Segment = ...

	@overload
	def __init__(self, src : CrossingLocation) -> None:
		...

	@overload
	def __init__(self, t1 : Segment, t2 : Segment) -> None:
		...

	@overload
	def preferedOrder(self, e1 : edge, e2 : edge) -> bool:
		...

	@overload
	def preferedOrder(self, s1 : Segment, s2 : Segment) -> bool:
		...
