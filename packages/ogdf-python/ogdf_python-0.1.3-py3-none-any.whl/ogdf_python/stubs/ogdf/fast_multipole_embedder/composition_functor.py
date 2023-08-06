# file stubs/ogdf/fast_multipole_embedder/composition_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1composition__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
FuncFirst = TypeVar('FuncFirst')

B = TypeVar('B')

FuncSecond = TypeVar('FuncSecond')

A = TypeVar('A')

class composition_functor(Generic[FuncFirst, FuncSecond]):

	"""Functor for composing two other functors."""

	firstFunc : FuncFirst = ...

	secondFunc : FuncSecond = ...

	def __init__(self, first : FuncFirst, second : FuncSecond) -> None:
		...

	@overload
	def __call__(self, a : A) -> None:
		...

	@overload
	def __call__(self, a : A, b : B) -> None:
		...
