# file stubs/ogdf/fast_multipole_embedder/pair_call_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1pair__call__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

B = TypeVar('B')

A = TypeVar('A')

class pair_call_functor(Generic[F, A]):

	"""helper functor to generate a pair as parameters"""

	first : A = ...

	func : F = ...

	def __init__(self, f : F, a : A) -> None:
		...

	def __call__(self, second : B) -> None:
		...
