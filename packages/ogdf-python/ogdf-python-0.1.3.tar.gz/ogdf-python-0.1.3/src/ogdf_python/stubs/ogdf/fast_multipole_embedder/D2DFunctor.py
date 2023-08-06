# file stubs/ogdf/fast_multipole_embedder/D2DFunctor.py generated from classogdf_1_1fast__multipole__embedder_1_1_d2_d_functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class D2DFunctor(object):

	"""Calculates the repulsive forces acting between all nodes of the direct interacting cells of the i-th node."""

	def __init__(self, pLocalContext : FMELocalContext) -> None:
		...

	@overload
	def __call__(self, begin : int, end : int) -> None:
		...

	@overload
	def __call__(self, i : int) -> None:
		...

	@overload
	def __call__(self, _ : None) -> int:
		...
