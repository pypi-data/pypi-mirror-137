# file stubs/ogdf/OrderedOptimalCrossingMinimizer/CrossingVariableBase.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_crossing_variable_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingVariableBase(abacus.Variable):

	e : ctwoEdge = ...

	def __init__(self, m : abacus.Master, cost : float, t1 : edge, t2 : edge, tLocal : bool = False) -> None:
		...
