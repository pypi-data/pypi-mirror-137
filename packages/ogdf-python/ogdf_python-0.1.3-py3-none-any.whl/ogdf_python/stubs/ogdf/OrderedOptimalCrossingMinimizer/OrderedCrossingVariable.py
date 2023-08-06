# file stubs/ogdf/OrderedOptimalCrossingMinimizer/OrderedCrossingVariable.py generated from classogdf_1_1_ordered_optimal_crossing_minimizer_1_1_ordered_crossing_variable
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrderedCrossingVariable(ogdf.OrderedOptimalCrossingMinimizer.CrossingVariableBase):

	def __init__(self, m : abacus.Master, _e : edge, _f : edge, _g : edge) -> None:
		...

	def base(self) -> edge:
		...

	def before(self) -> edge:
		...

	def crossedBy(self) -> edge:
		...

	def isTwin(self, t : OrderedCrossingVariable) -> bool:
		...

	def name(self) -> str:
		"""Should return the name of the constraint/variable."""
		...
