# file stubs/ogdf/OrderedOptimalCrossingMinimizer/SimpleCrossingVariable.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_simple_crossing_variable
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimpleCrossingVariable(ogdf.OrderedOptimalCrossingMinimizer.CrossingVariableBase):

	def __init__(self, m : abacus.Master, t1 : edge, t2 : edge) -> None:
		...

	def commonEdge(self, s : SimpleCrossingVariable) -> edge:
		...

	@overload
	def correspondsTo(self, ee : edge) -> bool:
		...

	@overload
	def correspondsTo(self, n : node) -> bool:
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...

	def otherEdge(self, ee : edge) -> edge:
		...

	def preferedOrder(self, e1 : edge, e2 : edge) -> bool:
		...
