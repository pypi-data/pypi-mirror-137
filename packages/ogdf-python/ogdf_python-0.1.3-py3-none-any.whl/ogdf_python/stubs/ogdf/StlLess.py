# file stubs/ogdf/StlLess.py generated from classogdf_1_1_stl_less
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
COMPARER = TypeVar('COMPARER')

TYPE = TypeVar('TYPE')

class StlLess(Generic[TYPE, COMPARER]):

	"""Template for converting anyStdComparerinto a STL compatible compare functor."""

	def __call__(self, x : TYPE, y : TYPE) -> bool:
		...
