# file stubs/ogdf/fast_multipole_embedder/NDFunctor.py generated from classogdf_1_1fast__multipole__embedder_1_1_n_d_functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NDFunctor(object):

	"""Calculates the repulsive forces acting between all nodes inside the cell of the i-thLinearQuadtreenode."""

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
