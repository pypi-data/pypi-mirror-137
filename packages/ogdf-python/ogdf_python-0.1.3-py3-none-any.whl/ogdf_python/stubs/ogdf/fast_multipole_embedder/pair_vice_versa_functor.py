# file stubs/ogdf/fast_multipole_embedder/pair_vice_versa_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1pair__vice__versa__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
B = TypeVar('B')

Func = TypeVar('Func')

A = TypeVar('A')

class pair_vice_versa_functor(Generic[Func]):

	"""functor for invoking a functor for a pair(u,v) and then (v,u)"""

	func : Func = ...

	def __init__(self, f : Func) -> None:
		...

	def __call__(self, a : A, b : B) -> None:
		...
