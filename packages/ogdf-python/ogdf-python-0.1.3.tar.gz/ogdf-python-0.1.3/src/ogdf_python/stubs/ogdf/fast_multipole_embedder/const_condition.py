# file stubs/ogdf/fast_multipole_embedder/const_condition.py generated from structogdf_1_1fast__multipole__embedder_1_1const__condition
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
B = TypeVar('B')

result = TypeVar('result')

A = TypeVar('A')

class const_condition(Generic[result]):

	"""condition functor for returning a constant boolean value"""

	@overload
	def __call__(self, a : A) -> bool:
		...

	@overload
	def __call__(self, a : A, b : B) -> bool:
		...
