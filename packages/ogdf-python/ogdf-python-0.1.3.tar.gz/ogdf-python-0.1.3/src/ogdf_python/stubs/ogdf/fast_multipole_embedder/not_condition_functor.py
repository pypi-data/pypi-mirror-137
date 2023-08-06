# file stubs/ogdf/fast_multipole_embedder/not_condition_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1not__condition__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
B = TypeVar('B')

Func = TypeVar('Func')

A = TypeVar('A')

class not_condition_functor(Generic[Func]):

	"""functor for negating a condition"""

	cond_func : Func = ...

	def __init__(self, cond : Func) -> None:
		...

	@overload
	def __call__(self, a : A) -> bool:
		...

	@overload
	def __call__(self, a : A, b : B) -> None:
		...
