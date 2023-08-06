# file stubs/ogdf/StlGreater.py generated from classogdf_1_1_stl_greater
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
COMPARER = TypeVar('COMPARER')

TYPE = TypeVar('TYPE')

class StlGreater(Generic[TYPE, COMPARER]):

	"""Template for converting anyStdComparerinto a STL compatible compare functor."""

	def __call__(self, x : TYPE, y : TYPE) -> bool:
		...
