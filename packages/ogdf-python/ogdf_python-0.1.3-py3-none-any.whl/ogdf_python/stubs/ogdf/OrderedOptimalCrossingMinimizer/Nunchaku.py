# file stubs/ogdf/OrderedOptimalCrossingMinimizer/Nunchaku.py generated from structogdf_1_1_ordered_optimal_crossing_minimizer_1_1_nunchaku
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Nunchaku(object):

	a : edge = ...

	b : edge = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, x : edge, y : edge) -> None:
		...

	@overload
	def __init__(self, n : Nunchaku) -> None:
		...

	def __assign__(self, n : Nunchaku) -> Nunchaku:
		...
