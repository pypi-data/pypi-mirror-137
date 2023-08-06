# file stubs/ogdf/OptimalCrossingMinimizer/Segment.py generated from structogdf_1_1_optimal_crossing_minimizer_1_1_segment
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Segment(object):

	e : edge = ...

	seg : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, src : Segment) -> None:
		...

	@overload
	def __init__(self, te : edge, tseg : int) -> None:
		...

	@overload
	def init(self, src : Segment) -> None:
		...

	@overload
	def init(self, te : edge, tseg : int) -> None:
		...

	def __eq__(self, s : Segment) -> int:
		...
