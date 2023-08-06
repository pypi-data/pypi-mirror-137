# file stubs/ogdf/optimal_crossing_minimizer/Base.py generated from classogdf_1_1optimal__crossing__minimizer_1_1_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
M = TypeVar('M')

T = TypeVar('T')

class Base(ogdf.CrossingMinimizationModule):

	EPS : float = ...

	SEG_EPS : float = ...

	def clone(self, blaster : M) -> T:
		...

	def free(self, pointer : T) -> None:
		"""Frees allocated memory and sets the pointer tonullptr."""
		...
