# file stubs/ogdf/OrderedOptimalCrossingMinimizer/CrossingVariableComparer.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_crossing_variable_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CrossingVariableComparer(object):

	CrossingVariablePointer : Type = CrossingVariableBase

	def compare(self, x : CrossingVariablePointer, y : CrossingVariablePointer) -> int:
		...
