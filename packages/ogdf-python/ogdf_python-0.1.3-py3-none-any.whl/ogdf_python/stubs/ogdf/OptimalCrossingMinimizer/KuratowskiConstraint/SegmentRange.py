# file stubs/ogdf/OptimalCrossingMinimizer/KuratowskiConstraint/SegmentRange.py generated from structogdf_1_1_optimal_crossing_minimizer_1_1_kuratowski_constraint_1_1_segment_range
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SegmentRange(object):

	endId : int = ...

	next : SegmentRange = ...

	pathNo : int = ...

	startId : int = ...

	@overload
	def __init__(self, E : SegmentRange) -> None:
		...

	@overload
	def __init__(self, s : int, e : int, path : int, _next : SegmentRange) -> None:
		...

	def __destruct__(self) -> None:
		...

	def contains(self, id : int) -> bool:
		...

	def equals(self, ei : SegmentRange) -> bool:
		...
