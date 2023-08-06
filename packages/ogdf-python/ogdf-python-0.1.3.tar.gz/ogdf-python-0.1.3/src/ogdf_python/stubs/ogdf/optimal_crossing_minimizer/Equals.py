# file stubs/ogdf/optimal_crossing_minimizer/Equals.py generated from classogdf_1_1optimal__crossing__minimizer_1_1_equals
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

class Equals(Generic[C]):

	def compare(self, a : C, b : C) -> int:
		...
