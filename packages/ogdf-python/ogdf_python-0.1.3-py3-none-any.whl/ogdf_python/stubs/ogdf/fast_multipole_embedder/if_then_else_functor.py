# file stubs/ogdf/fast_multipole_embedder/if_then_else_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1if__then__else__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ThenType = TypeVar('ThenType')

CondType = TypeVar('CondType')

A = TypeVar('A')

B = TypeVar('B')

ElseType = TypeVar('ElseType')

class if_then_else_functor(Generic[CondType, ThenType, ElseType]):

	"""Functor for conditional usage of a functor."""

	condFunc : CondType = ...

	elseFunc : ElseType = ...

	thenFunc : ThenType = ...

	@overload
	def __init__(self, c : CondType, f1 : ThenType) -> None:
		...

	@overload
	def __init__(self, c : CondType, f1 : ThenType, f2 : ElseType) -> None:
		...

	@overload
	def __call__(self, a : A) -> None:
		...

	@overload
	def __call__(self, a : A, b : B) -> None:
		...
