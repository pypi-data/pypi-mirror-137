# file stubs/ogdf/fast_multipole_embedder/M2LFunctor.py generated from classogdf_1_1fast__multipole__embedder_1_1_m2_l_functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class M2LFunctor(object):

	"""Converts the multipole expansion coefficients from all nodes which are well separated from the i-th node to local expansion coefficients and adds them to the local expansion coefficients of the i-th node."""

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
