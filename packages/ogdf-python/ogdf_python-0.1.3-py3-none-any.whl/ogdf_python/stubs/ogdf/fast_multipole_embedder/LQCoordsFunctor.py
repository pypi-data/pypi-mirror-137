# file stubs/ogdf/fast_multipole_embedder/LQCoordsFunctor.py generated from classogdf_1_1fast__multipole__embedder_1_1_l_q_coords_functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LQCoordsFunctor(object):

	"""Computes the coords and size of the i-th node in theLinearQuadtree."""

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
